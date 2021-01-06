from django.db import IntegrityError
from rest_framework.serializers import ModelSerializer

from django.contrib.auth import authenticate, login
from rest_framework import serializers

from diploma.apps.tasks.constants import REGISTRATION_HEADER, REGISTRATION_TEXT
from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.user.models import MasterUser


class RetrieveUserSerializer(ModelSerializer):
	class Meta:
		model = MasterUser
		fields = [
			'id',
			'email',
			'phone_number',
			'first_name',
			'last_name',
			'photo',
			'is_staff',
			'is_deleted',
			'is_master'
		]


class ShowUsersSerializer(ModelSerializer):
	class Meta:
		model = MasterUser
		fields = [
			'id',
			'email',
			'phone_number',
			'first_name',
			'last_name',
		]


class RegistrationSerializer(ModelSerializer):
	repeated_password = serializers.CharField(
		min_length=3,
		max_length=100,
		required=True,
		allow_blank=False,
		allow_null=False
	)

	class Meta:
		model = MasterUser
		fields = [
			'email',
			'password',
			'phone_number',
			'first_name',
			'last_name',
			'repeated_password',
			'photo',
			'is_master'
		]
		extra_kwargs = {
			'photo': {
				'required': False
			},
			'is_master': {
				'required': False
			},
			'phone_number': {
				'required': False
			},
			'first_name': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'last_name': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'password': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False,
				'write_only': True
			},
			'email': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
		}

	def _validate_password(self, attrs):
		password = attrs.get('password')
		repeated_password = attrs.get('repeated_password')
		if password != repeated_password:
			raise serializers.ValidationError('Password and repeated password are not the same')

	def validate(self, attrs):
		if not attrs.get('username', None):
			attrs['username'] = attrs.get('email')
		self._validate_password(attrs)
		return attrs

	def send_email(self, user):
		send_email(REGISTRATION_HEADER, REGISTRATION_TEXT, user)

	def save(self):
		try:
			user = MasterUser.objects.create_user(
				username=self.validated_data['username'],
				email=self.validated_data['email'],
				password=self.validated_data['password'],
			)
		except IntegrityError:
			raise serializers.ValidationError('User with that email has already exists')
		else:
			user.first_name = self.validated_data['first_name']
			user.last_name = self.validated_data['last_name']
			user.phone_number = self.validated_data.get('phone_number')
			user.photo = self.validated_data.get('photo')
			user.is_master = self.validated_data.get('is_master', False)
			user.save(update_fields=['first_name', 'last_name', 'phone_number', 'photo', 'is_master'])
			self.send_email(user)
			return user


class LoginSerializer(ModelSerializer):
	class Meta:
		model = MasterUser
		fields = [
			'email',
			'password',
		]
		extra_kwargs = {
			'password': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False,
				'write_only': True
			},
			'email': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			}
		}

	def save(self):
		user = authenticate(username=self.validated_data['email'], password=self.validated_data['password'])
		if user:
			login(request=self.context['view'].request, user=user)
			if user.is_deleted:
				raise serializers.ValidationError(
					'The password is valid, but the account has been disabled!'
				)
		else:
			raise serializers.ValidationError('The username or password were incorrect')
		return user
