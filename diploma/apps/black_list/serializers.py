from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma.apps.black_list.constants import BLACK_LIST_HEADER, BLACK_LIST_ADD_TEXT
from diploma.apps.black_list.models import BlackList
from diploma.apps.tasks.mail_sending import send_email


class RemoveBlackListNoteSerializer(ModelSerializer):
	class Meta:
		model = BlackList
		fields = [
			'address',
			'email',
			'phone',
		]


class CreateBlackListNoteViewSerializer(ModelSerializer):
	class Meta:
		model = BlackList
		fields = [
			'address',
			'email',
			'phone',
		]
		extra_kwargs = {
			'address': {
				'required': False,
				'allow_blank': False,
			},
			'email': {
				'required': False,
				'allow_blank': False,
			},
			'phone': {
				'required': False,
				'allow_blank': False,
			},
		}

	def _validate_email_phone(self, attrs):
		if not attrs.get('email') and not attrs.get('phone'):
			raise serializers.ValidationError(
				'You have to provide email or phone'
			)

	def validate(self, attrs):
		self._validate_email_phone(attrs)
		return attrs

	def _send_email_to_user(self, instance):
		if instance.email:
			send_email(BLACK_LIST_HEADER, BLACK_LIST_ADD_TEXT, user=None, user_email=instance.email)

	def create(self, validated_data):
		instance = super(CreateBlackListNoteViewSerializer, self).create(validated_data)
		self._send_email_to_user(instance)
		return instance
