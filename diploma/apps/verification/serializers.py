import random
import hashlib

from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.tasks.sms_sending import send_sms_task
from diploma.apps.verification.constants import BUFFER_PERIOD_VERIFICATION, EMAIL_HEADER
from diploma.apps.verification.models import VerificationClass


class CommonVerifySerializer(ModelSerializer):

	def _validate_email_phone(self, attrs):
		if not attrs.get('email') and not attrs.get('phone'):
			raise serializers.ValidationError(
				'You have to provide email or phone'
			)

	def get_existing_instance(self, attrs):
		existing_code = None
		if attrs.get('phone') and VerificationClass.objects.filter(phone=attrs.get('phone')).exists():
			existing_code = VerificationClass.objects.get(phone=attrs.get('phone'))
		elif VerificationClass.objects.filter(email=attrs.get('email')).exists():
			existing_code = VerificationClass.objects.get(email=attrs.get('email'))
		return existing_code

	def validate(self, attrs):
		self._validate_email_phone(attrs)
		return attrs


class VerifyCodeSerializer(CommonVerifySerializer):
	code = serializers.IntegerField(write_only=True, required=True)

	class Meta:
		model = VerificationClass
		fields = [
			'email',
			'phone',
			'code',
		]
		extra_kwargs = {
			'email': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'phone': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
		}

	def _validate_existence(self, attrs):
		if not self.get_existing_instance(attrs):
			raise serializers.ValidationError(
				'There is now code for that email or phone'
			)

	def _validate_time(self, attrs):
		existing_code = self.get_existing_instance(attrs)
		if existing_code.sending_time + BUFFER_PERIOD_VERIFICATION < timezone.now():
				raise serializers.ValidationError(
					'Your verification code has expired, please request it again'
				)

	def _validate_authoring(self, attrs):
		existing_code = self.get_existing_instance(attrs)
		if existing_code.is_authorize:
			raise serializers.ValidationError(
				'You need to ask for code once again'
			)

	def _validate_code(self, attrs):
		code = attrs.pop('code')
		hash = hashlib.md5(str(code))
		existing_hash = self.get_existing_instance(attrs).code_hash
		if hash != existing_hash:
			raise serializers.ValidationError(
				'Your code is incorrect, try again please'
			)

	def validate(self, attrs):
		attrs = super(VerifyCodeSerializer, self).validate(attrs)
		self._validate_existence(attrs)
		self._validate_time(attrs)
		self._validate_authoring(attrs)
		self._validate_code(attrs)
		return attrs

	def create(self, validated_data):
		if validated_data.get('phone'):
			VerificationClass.objects.filter(phone=validated_data.get('phone')).\
				update(is_authorize=True, authorizing_time=timezone.now())
		else:
			VerificationClass.objects.filter(email=validated_data.get('email')).\
				update(is_authorize=True, authorizing_time=timezone.now())
		return self.get_existing_instance(validated_data)


class RequestForCodeSerializer(CommonVerifySerializer):

	class Meta:
		model = VerificationClass
		fields = [
			'email',
			'phone',
			'code_hash',
		]
		extra_kwargs = {
			'code_hash': {
				'read_only': True,
				'required': False,
			},
			'email': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'phone': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
		}

	def _validate_time(self, attrs):
		existing_code = self.get_existing_instance(attrs)
		if existing_code and existing_code.sending_time + BUFFER_PERIOD_VERIFICATION < timezone.now():
				raise serializers.ValidationError(
					'Please wait before asking for code again'
				)

	def validate(self, attrs):
		attrs = super(RequestForCodeSerializer, self).validate(attrs)
		self._validate_time(attrs)
		return attrs

	def create(self, validated_data):
		code = random.randint(1000, 9999)
		code_hash = hashlib.md5(str(code))
		if validated_data.get('phone'):
			send_sms_task(code_hash, validated_data.get('phone'))
			instance, _ = VerificationClass.objects.update_or_create(
				phone=validated_data.get('phone'),
				defaults={
					'code_hash': code_hash,
					'sending_time': timezone.now(),
					'is_authorize': False
				},
			)
		else:
			send_email(
				EMAIL_HEADER, f'Hello, your verification code is {code}',
				user=None,
				user_email=validated_data.get('email')
			)
			instance, _ = VerificationClass.objects.update_or_create(
				email=validated_data.get('email'),
				defaults={
					'code_hash': code_hash,
					'sending_time': timezone.now(),
					'is_authorize': False
				},
			)
		return instance


