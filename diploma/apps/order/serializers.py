import os

from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma import settings
from diploma.apps.black_list.models import BlackList
from diploma.apps.order.constants import Statuses, BUFFER_PERIOD, ORDER_REQUEST_HEADER, ORDER_REQUEST_TEXT, \
	ORDER_PHOTO_DIR
from diploma.apps.order.models import WorkOrder
from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.works.models import Work


class CommonOrderSerializer(ModelSerializer):

	def _validate_time_period(self, date_time_of_work_begin, work):
		if date_time_of_work_begin:
			if not work:
				if self.instance:
					work = self.instance.id
				else:
					raise serializers.ValidationError(
						'You need to specify work'
					)
			if WorkOrder.objects.filter(
					Q(work=work) & Q(status=Statuses.APPROVED) &
					(
						Q(date_time_of_work_begin__lte=date_time_of_work_begin + BUFFER_PERIOD) & Q(
							date_time_of_work_begin__gte=date_time_of_work_begin) |
						Q(date_time_of_work_begin__gte=date_time_of_work_begin - BUFFER_PERIOD) & Q(
							date_time_of_work_begin__lte=date_time_of_work_begin)
					)
			).exists() or date_time_of_work_begin < timezone.now():
				raise serializers.ValidationError(
					'This time is not available for ordering'
				)

	def _validate_customer(self, attrs):
		if self.context['request'].user:
			attrs['customer_id'] = self.context['request'].user.id
			if not attrs.get('customer_phone'):
				attrs['customer_phone'] = self.context['request'].user.phone_number
			if not attrs.get('customer_email'):
				attrs['customer_email'] = self.context['request'].user.email
		return attrs

	def _validate_phone_email(self, attrs):
		if not attrs.get('customer_phone') and not attrs.get('customer_email'):
			raise serializers.ValidationError(
				'You have to specify customer_phone or customer_email'
			)

	def _validate_black_list(self, attrs):
		if attrs.get('customer_phone') and BlackList.objects.filter(phone=attrs.get('customer_phone')):
			raise serializers.ValidationError(
				'That phone is in black list'
			)
		if attrs.get('customer_email') and BlackList.objects.filter(email=attrs.get('customer_email')):
			raise serializers.ValidationError(
				'That email is in black list'
			)
		if attrs.get('address') and BlackList.objects.filter(address=attrs.get('address')):
			raise serializers.ValidationError(
				'That address is in black list'
			)

	def validate(self, attrs):
		attrs = self._validate_customer(attrs)
		self._validate_phone_email(attrs)
		self._validate_time_period(attrs.get('date_time_of_work_begin'), attrs.get('work'))
		self._validate_black_list(attrs)
		return attrs


class UpdateOrderSerializer(CommonOrderSerializer):
	date_time_of_work_begin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

	class Meta:
		model = WorkOrder
		fields = [
			'id',
			'date_time_of_work_begin',
			'customer_phone',
			'customer_text_comment',
			'customer_email',
			'address',
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'customer_text_comment': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'customer_phone': {
				'required': False,
				'allow_blank': False
			},
			'date_time_of_work_begin': {
				'required': False,
				'allow_blank': False,
				'allow_null': False
			},
			'customer_email': {
				'required': False,
				'allow_blank': False
			},
			'address': {
				'required': False,
				'allow_blank': False
			},
		}


class ListOrderSerializer(ModelSerializer):
	date_time_of_work_begin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	work = serializers.PrimaryKeyRelatedField(queryset=Work.active_objects.all())

	class Meta:
		model = WorkOrder
		fields = [
			'date_time_of_work_begin',
			'work',
			'date_of_creating_request',
			'address'
		]
		extra_kwargs = {
			'address': {
				'required': False,
				'allow_blank': False
			},
			'date_of_creating_request': {
				'read_only': True,
			},
			'date_time_of_work_begin': {
				'allow_blank': False,
				'allow_null': False,
				'read_only': True,
			},
			'work': {
				'allow_null': False,
				'read_only': True,
			},
		}


class RetrieveOrderSerializer(ModelSerializer):
	photos = serializers.ListField(child=serializers.ImageField())
	date_time_of_work_begin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	work = serializers.PrimaryKeyRelatedField(queryset=Work.active_objects.all())

	class Meta:
		model = WorkOrder
		fields = [
			'date_time_of_work_begin',
			'customer_phone',
			'customer_text_comment',
			'customer_email',
			'address',
			'work',
			'photos',
			'date_of_creating_request'
		]
		extra_kwargs = {
			'customer_text_comment': {
				'allow_blank': True,
				'allow_null': True,
				'read_only': True,
			},
			'date_of_creating_request': {
				'read_only': True,
			},
			'customer_phone': {
				'allow_blank': False,
				'read_only': True,
			},
			'date_time_of_work_begin': {
				'allow_blank': False,
				'allow_null': False,
				'read_only': True,
			},
			'customer_email': {
				'allow_blank': False,
				'read_only': True,
			},
			'address': {
				'allow_blank': False,
				'read_only': True,
			},
			'work': {
				'allow_null': False,
				'read_only': True,
			},
			'photos': {
				'allow_null': False,
				'read_only': True,
			}
		}

	def _get_path_to_photo(self, photo_name):
		return os.path.join(settings.MEDIA_ROOT, ORDER_PHOTO_DIR, photo_name)

	def to_representation(self, instance):
		representation_result = super(RetrieveOrderSerializer, self).to_representation(instance)
		if representation_result.get('photos'):
			representation_result['photos'].clear()
			for photo in instance.photos:
				representation_result['photos'].append(self._get_path_to_photo(photo))
		return representation_result


class CreateOrderSerializer(CommonOrderSerializer):
	photos = serializers.ListField(child=serializers.ImageField(), required=False)
	date_time_of_work_begin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	work = serializers.PrimaryKeyRelatedField(queryset=Work.active_objects.all())

	class Meta:
		model = WorkOrder
		fields = [
			'id',
			'work',
			'date_time_of_work_begin',
			'customer_phone',
			'customer_text_comment',
			'customer_email',
			'address',
			'photos'
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'work': {
				'required': True,
				'allow_null': False
			},
			'customer_text_comment': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'customer_phone': {
				'required': False,
				'allow_blank': False
			},
			'date_time_of_work_begin': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'customer_email': {
				'required': False,
				'allow_blank': False
			},
			'address': {
				'required': False,
				'allow_blank': False
			},
			'photos': {
				'required': False,
			},
		}

	def _get_path_to_photo(self, photo_name):
		return os.path.join(settings.MEDIA_ROOT, ORDER_PHOTO_DIR, photo_name)

	def _upload_photos(self, validated_data):
		photos = validated_data.get('photos')
		if photos:
			for photo in photos:
				absolute_file_path = self._get_path_to_photo(photo.name)
				with open(absolute_file_path, 'wb') as f:
					f.write(photo.file.read())

	def to_representation(self, instance):
		representation_result = super(CreateOrderSerializer, self).to_representation(instance)
		if representation_result.get('photos'):
			representation_result['photos'].clear()
			for photo in instance.photos:
				representation_result['photos'].append(self._get_path_to_photo(photo.name))
		return representation_result

	def create(self, validated_data):
		self._upload_photos(self.validated_data)
		instance = super(CreateOrderSerializer, self).create(validated_data)
		send_email(header=ORDER_REQUEST_HEADER, text=ORDER_REQUEST_TEXT, user=instance.work.worker)
		return instance
