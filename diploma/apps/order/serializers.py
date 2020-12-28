from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma.apps.order.constants import Statuses, BUFFER_PERIOD, ORDER_REQUEST_HEADER, ORDER_REQUEST_TEXT
from diploma.apps.order.models import WorkOrder
from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.works.models import Work


class CreateOrderSerializer(ModelSerializer):
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

	def _validate_time_period(self, date_time_of_work_begin, work):
		if WorkOrder.objects.filter(
				Q(work=work) & Q(status=Statuses.APPROVED) &
				Q(date_time_of_rent_begin__lte=date_time_of_work_begin + BUFFER_PERIOD) & Q(
					date_time_of_rent_begin__gte=date_time_of_work_begin) |
				Q(date_time_of_rent_begin__gte=date_time_of_work_begin - BUFFER_PERIOD) & Q(
					date_time_of_rent_end__lte=date_time_of_work_begin)
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
		pass
		#add validation from black list

	def validate(self, attrs):
		attrs = self._validate_customer(attrs)
		self._validate_phone_email(attrs)
		self._validate_time_period(attrs['date_time_of_work_begin'], attrs['work'])
		self._validate_black_list(attrs)
		return attrs

	def save(self):
		super(CreateOrderSerializer, self).is_valid(raise_exception=True)
		instance = super(CreateOrderSerializer, self).save()
		send_email(header=ORDER_REQUEST_HEADER, text=ORDER_REQUEST_TEXT, user=instance.work.worker)
		return instance
