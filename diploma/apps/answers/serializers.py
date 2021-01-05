from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from diploma.apps.answers.constants import ANSWER_ORDER_REQUEST_TEXT_BEGIN, ANSWER_ORDER_REQUEST_TEXT_END, \
	ANSWER_ORDER_REQUEST_HEADER, ANSWER_COMPLAINT_TEXT, ANSWER_COMPLAINT_HEADER
from diploma.apps.answers.models import OrderAnswer, ComplaintAnswer
from diploma.apps.order.constants import Statuses, ANSWER_STATUSES
from diploma.apps.order.models import WorkOrder
from diploma.apps.reactions.models import Complaint
from diploma.apps.tasks.mail_sending import send_email


class CreateComplaintAnswerSerializer(ModelSerializer):

	complaint = serializers.PrimaryKeyRelatedField(queryset=Complaint.objects.filter(status=Statuses.IN_PROCESS))
	status = serializers.CharField(max_length=10, write_only=True)

	class Meta:
		model = ComplaintAnswer
		fields = [
			'complaint',
			'text',
			'status',
			'answered_admin'
		]
		extra_kwargs = {
			'id': {
				'read_only': True,
				'required': False,
			},
			'answered_admin': {
				'required': False,
				'allow_null': False
			},
			'text': {
				'required': False,
				'allow_blank': False,
				'allow_null': False
			},
			'complaint': {
				'required': True,
				'allow_blank': False,
				'allow_null': False,
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

	def _add_user(self, attrs):
		user = self.context['request'].user
		attrs['answered_admin'] = user

	def validate(self, attrs):
		self._validate_status(attrs)
		self._add_user(attrs)
		return attrs

	def _change_complaint_status(self, validated_data):
		try:
			complaint = validated_data.get('complaint')
			status = validated_data.pop('status')
			complaint.status = status
			complaint.save(update_fields=['status'])
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not answer that order'
			)
		return status

	def _send_email_to_user(self, instance, status):
		text = ANSWER_COMPLAINT_TEXT + status
		send_email(ANSWER_COMPLAINT_HEADER, text, user=instance.complaint.complaint_creater)

	def create(self, validated_data):
		status = self._change_complaint_status(validated_data)
		instance = super(CreateComplaintAnswerSerializer, self).create(validated_data)
		self._send_email_to_user(instance, status)
		return instance


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
