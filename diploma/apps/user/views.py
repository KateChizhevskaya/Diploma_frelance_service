from django.contrib.auth import logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.user.constants import DELETE_USER_HEADER, DELETE_USER_TEXT
from diploma.apps.user.models import MasterUser
from diploma.apps.user.serializers import RegistrationSerializer, LoginSerializer, ShowUsersSerializer, \
	RetrieveUserSerializer, UpdateUserSerializer, AdminUpdateUserSerializer


class RegistrationView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer


class LogoutView(APIView):

	def post(self, request, *args, **kwargs):
		if not self.request.user.is_anonymous:
			logout(request)
			return Response(status=status.HTTP_200_OK)
		else:
			raise ValidationError(
				'You need to login first'
			)


class LoginView(generics.CreateAPIView):
	serializer_class = LoginSerializer


class DeleteUserView(generics.DestroyAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser,)

	def get_object(self):
		if not self.request.user.is_staff:
			raise ValidationError(
				'You need to be admin'
			)
		if not self.request.user.is_anonymous:
			try:
				user = MasterUser.objects.get(id=self.kwargs['id'])
				if user.email != self.request.user.email:
					return user
				else:
					raise ValidationError(
						'You can not delete your self'
					)
			except MasterUser.DoesNotExist:
				raise ValidationError(
					'You can not delete that user'
				)
		else:
			raise ValidationError(
				'You need to login first'
			)

	def send_email(self, instance):
		send_email(DELETE_USER_HEADER, DELETE_USER_TEXT, user=None, user_email=instance.email)

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save(update_fields=['is_deleted'])
		self.send_email(instance)


class UpdateUserView(generics.UpdateAPIView):
	permissions = (permissions.IsAuthenticated, )
	serializer_class = UpdateUserSerializer

	def get_object(self):
		if self.request.user.is_authenticated:
			try:
				return MasterUser.objects.get(email=self.request.user.email)
			except MasterUser.DoesNotExist:
				raise ValidationError(
					'You can not update not yourself'
				)
		else:
			raise ValidationError(
				'You need to log in'
			)


class AdminUpdateUser(generics.UpdateAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser)
	serializer_class = AdminUpdateUserSerializer

	def get_object(self):
		if not self.request.user.is_anonymous:
			try:
				user = MasterUser.objects.get(id=self.kwargs['id'])
				if user.email != self.request.user.email:
					return user
				else:
					raise ValidationError(
						'You can not update your self'
					)
			except MasterUser.DoesNotExist:
				raise ValidationError(
					'You can not update that user'
				)

		else:
			raise ValidationError(
				'You need to login first'
			)


class ListUsersView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = ShowUsersSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['email', 'is_staff', 'is_master', 'is_deleted']
	queryset = MasterUser.objects.all()


class RetrieveUsersView(generics.RetrieveAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = RetrieveUserSerializer
	lookup_field = 'id'
	queryset = MasterUser.objects.all()
