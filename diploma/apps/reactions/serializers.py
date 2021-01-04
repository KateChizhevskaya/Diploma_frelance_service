import os

from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma import settings
from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.reactions.constants import REVIEW_PHOTO_DIR
from diploma.apps.reactions.models import Review
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
		photos = validated_data['photos']
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
		instance = super(AddReviewSerializer, self).create(validated_data)
		self.recalculate_work_raiting(instance)
		return instance
