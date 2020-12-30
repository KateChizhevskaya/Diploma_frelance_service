from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from diploma.apps.answers.constants import ANSWER_ORDER_REQUEST_TEXT_BEGIN, ANSWER_ORDER_REQUEST_TEXT_END, \
	ANSWER_ORDER_REQUEST_HEADER
from diploma.apps.answers.models import OrderAnswer
from diploma.apps.order.constants import Statuses, ANSWER_STATUSES
from diploma.apps.order.models import WorkOrder
from diploma.apps.tasks.mail_sending import send_email


class CreateOrderAnswerSerializer(ModelSerializer):
	order = serializers.PrimaryKeyRelatedField(queryset=WorkOrder.unapproved_objects.all())
	status = serializers.CharField(max_length=10, write_only=True)

	class Meta:
		model = OrderAnswer
		fields = [
			'order',
			'text',
			'status'
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'text': {
				'required': False,
				'allow_blank': False,
				'allow_null': False
			},
			'order': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'status': {
				'required': True,
				'allow_blank': False,
				'allow_null': False,
				'write_only': True
			}
		}

	def _validate_status(self, attrs):
		if attrs.get('status') not in ANSWER_STATUSES:
			raise serializers.ValidationError(
				'Available statuses are approved or rejected'
			)

	def validate(self, attrs):
		self._validate_status(attrs)
		return attrs

	def _change_order_status(self, validated_data):
		try:
			order = validated_data.get('order')
			status = validated_data.pop('status')
			order.status = status
			order.save(update_fields=['status'])
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not answer that order'
			)
		return status

	def _send_email_to_customer(self, instance, status):
		if instance.order.customer_email:
			text = ANSWER_ORDER_REQUEST_TEXT_BEGIN + instance.order.work.name + ANSWER_ORDER_REQUEST_TEXT_END + status
			send_email(ANSWER_ORDER_REQUEST_HEADER, text, user=None, user_email=instance.order.customer_email)

	def create(self, validated_data):
		status = self._change_order_status(validated_data)
		instance = super(CreateOrderAnswerSerializer, self).create(validated_data)
		self._send_email_to_customer(instance, status)
		return instance
