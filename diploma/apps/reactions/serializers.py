import os

from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma import settings
from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.reactions.constants import REVIEW_PHOTO_DIR, COMPLAINT_DOCUMENT_DIR, COMPLAINT_PHOTO_DIR, \
	COMPLAINT_HEADER, COMPLAINT_TEXT, COMPLAINT_ADMIN_TEXT
from diploma.apps.reactions.models import Review, Complaint
from diploma.apps.tasks.mail_sending import send_email, send_mails_to_many_users
from diploma.apps.user.models import MasterUser
from diploma.apps.works.models import Work


class CommonReviewSerializer(ModelSerializer):

	def _validate_rating(self, attrs):
		rating = attrs.get('rating')
		if rating is not None and (rating > 5 or rating < 0):
			raise serializers.ValidationError(
				'Rating can be from 0 to 5'
			)

	def _get_path_to_photo(self, photo_name):
		return os.path.join(settings.MEDIA_ROOT, REVIEW_PHOTO_DIR, photo_name)

	def recalculate_work_raiting(self, instance):
		work = instance.work
		work_reviews = list(filter(
			lambda rating: rating is not None,
			Review.objects.filter(work=work).values_list('rating', flat=True)
		))
		work.rating = sum(map(lambda str_num: int(str_num), work_reviews)) / len(work_reviews)
		work.save(update_fields=('rating', ))


class ReviewShowSerializer(CommonReviewSerializer):
	class Meta:
		model = Review
		fields = [
			'id',
			'user',
			'rating',
			'text',
			'photos'
		]

	def to_representation(self, instance):
		representation_result = super(ReviewShowSerializer, self).to_representation(instance)
		if representation_result.get('photos'):
			representation_result['photos'].clear()
			for photo in instance.photos:
				representation_result['photos'].append(self._get_path_to_photo(photo))
		return representation_result


class UpdateReviewSerializer(CommonReviewSerializer):
	class Meta:
		model = Review
		fields = [
			'rating',
			'text',
		]

	def validate(self, attrs):
		self._validate_rating(attrs)
		return attrs

	def update(self, instance, validated_data):
		instance = super(UpdateReviewSerializer, self).update(instance, validated_data)
		self.recalculate_work_raiting(instance)
		return instance


class CommonComplaintSerializer(ModelSerializer):

	def _get_path_to_photo(self, photo_name):
		return os.path.join(settings.MEDIA_ROOT, COMPLAINT_PHOTO_DIR, photo_name)

	def _get_path_to_doc(self, doc_name):
		return os.path.join(settings.MEDIA_ROOT, COMPLAINT_DOCUMENT_DIR, doc_name)

	function_dict = {
		"photos": _get_path_to_photo,
		"documents": _get_path_to_doc
	}

	def _upload_file(self, file_obj, name, function_name):
		absolute_file_path = self.function_dict[function_name](self, name)
		with open(absolute_file_path, 'wb') as f:
			f.write(file_obj.file.read())


class RetrieveComplaintSerializer(CommonComplaintSerializer):

	class Meta:
		model = Complaint
		fields = [
			'id',
			'status',
			'date_of_creating_complaint',
			'text',
			'defendant_email',
			'defendant_phone',
			'defendant_address',
			'documents',
			'photos'
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'defendant_email': {
				'read_only': True,
				'required': False,
			},
			'defendant_phone': {
				'read_only': True,
				'required': False,
			},
			'defendant_address': {
				'read_only': True,
				'required': False,
			},
			'documents': {
				'read_only': True,
				'required': False,
			},
			'photos': {
				'read_only': True,
				'required': False,
			},
			'text': {
				'read_only': True,
				'required': False,
			},
			'status': {
				'read_only': True,
				'required': False,
			},
			'date_of_creating_complaint': {
				'read_only': True,
				'required': False,
			}
		}

	def _upload_photos_documents(self, validated_data):
		if validated_data.get('photos'):
			for item in validated_data['photos']:
				self._upload_file(item, item.name, 'photos')
		if validated_data.get('documents'):
			for item in validated_data['documents']:
				self._upload_file(item, item.name, 'documents')

	def _representation_file(self, name, representation_result, instance):
		if representation_result.get(name):
			representation_result[name].clear()
			for file in getattr(instance, name):
				representation_result[name].append(self.function_dict[name](self, file))

	def to_representation(self, instance):
		representation_result = super(RetrieveComplaintSerializer, self).to_representation(instance)
		for name in ('photos', 'documents'):
			self._representation_file(name, representation_result, instance)
		return representation_result


class ListComplaintSerializer(ModelSerializer):
	class Meta:
		model = Complaint
		fields = [
			'id',
			'status',
			'date_of_creating_complaint',
			'text',
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'text': {
				'read_only': True,
				'required': False,
			},
			'status': {
				'read_only': True,
				'required': False,
			},
			'date_of_creating_complaint': {
				'read_only': True,
				'required': False,
			}
		}


class AddComplaintSerializer(CommonComplaintSerializer):

	class Meta:
		model = Complaint
		fields = [
			'id',
			'defendant_email',
			'defendant_phone',
			'defendant_address',
			'text',
			'documents',
			'photos'
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'text': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'defendant_phone': {
				'required': False,
				'allow_blank': False
			},
			'defendant_email': {
				'required': False,
				'allow_blank': False
			},
			'defendant_address': {
				'required': False,
				'allow_blank': False
			},
			'photos': {
				'required': False,
			},
			'documents': {
				'required': False,
			}
		}

	def _add_user(self, attrs):
		user = self.context['request'].user
		attrs['complaint_creater'] = user

	def _validate_phone_email(self, attrs):
		if not attrs.get('defendant_phone') and not attrs.get('defendant_email'):
			raise serializers.ValidationError(
				'You have to specify defendant_phone or defendant_email'
			)

	def validate(self, attrs):
		self._validate_phone_email(attrs)
		self._add_user(attrs)
		return attrs

	def _upload_photos_documents(self, validated_data):
		if validated_data.get('photos'):
			for item in validated_data['photos']:
				self._upload_file(item, item.name, 'photos')
		if validated_data.get('documents'):
			for item in validated_data['documents']:
				self._upload_file(item, item.name, 'documents')

	def _representation_file(self, name, representation_result, instance):
		if representation_result.get(name):
			representation_result[name].clear()
			for file in getattr(instance, name):
				representation_result[name].append(self.function_dict[name](self, file.name))

	def to_representation(self, instance):
		representation_result = super(AddComplaintSerializer, self).to_representation(instance)
		for name in ('photos', 'documents'):
			self._representation_file(name, representation_result, instance)
		return representation_result

	def _send_email_to_all_admins(self):
		admins = MasterUser.objects.filter(is_staff=True)
		send_mails_to_many_users(header=COMPLAINT_HEADER, text=COMPLAINT_ADMIN_TEXT, users=admins)

	def create(self, validated_data):
		self._upload_photos_documents(self.validated_data)
		instance = super(AddComplaintSerializer, self).create(validated_data)
		send_email(header=COMPLAINT_HEADER, text=COMPLAINT_TEXT, user=instance.complaint_creater)
		self._send_email_to_all_admins()
		return instance


class AddReviewSerializer(CommonReviewSerializer):
	work = serializers.PrimaryKeyRelatedField(queryset=Work.active_objects.all())

	class Meta:
		model = Review
		fields = [
			'id',
			'user',
			'rating',
			'text',
			'work',
			'photos'
		]
		extra_kwargs = {
			'user': {
				'required': False,
			},
			'text': {
				'required': False,
			},
			'animal': {
				'required': True,
			},
			'rating': {
				'required': False
			},
			'photos': {
				'required': False
			}
		}

	def _validate_together(self, attrs):
		if attrs.get('text') is None and attrs.get('rating') is None:
			raise serializers.ValidationError(
				'You have to implement text or rating'
			)

	def _validate_work(self, attr):
		work = attr.get('work')
		user = self.context['request'].user
		if not WorkOrder.objects.filter(
			Q(status=Statuses.APPROVED) &
			Q(work=work) &
			(Q(customer=user) | Q(customer_email=user.email))
		).exists():
			raise serializers.ValidationError(
				'You can not add comment to work, that you have not ordered yet'
			)

	def _add_user(self, attrs):
		user = self.context['request'].user
		attrs['user'] = user

	def validate(self, attrs):
		self._validate_together(attrs)
		self._validate_rating(attrs)
		self._validate_work(attrs)
		self._add_user(attrs)
		return attrs

	def _upload_photos(self, validated_data):
		photos = validated_data.get('photos')
		if photos:
			for photo in photos:
				absolute_file_path = self._get_path_to_photo(photo.name)
				with open(absolute_file_path, 'wb') as f:
					f.write(photo.file.read())

	def to_representation(self, instance):
		representation_result = super(AddReviewSerializer, self).to_representation(instance)
		if representation_result.get('photos'):
			representation_result['photos'].clear()
			for photo in instance.photos:
				representation_result['photos'].append(self._get_path_to_photo(photo.name))
		return representation_result

	def create(self, validated_data):
		self._upload_photos(self.validated_data)
		instance = super(AddReviewSerializer, self).create(validated_data)
		self.recalculate_work_raiting(instance)
		return instance
