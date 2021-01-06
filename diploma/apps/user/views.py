
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from diploma.apps.tasks.mail_sending import send_email
from diploma.apps.user.constants import DELETE_USER_HEADER, DELETE_USER_TEXT
from diploma.apps.user.models import MasterUser
from diploma.apps.user.serializers import RegistrationSerializer, LoginSerializer, ShowUsersSerializer, \
	RetrieveUserSerializer


class RegistrationView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
	serializer_class = LoginSerializer


class DeleteUserView(generics.DestroyAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser,)

	def get_object(self):
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

	def send_email(self, instance):
		send_email(DELETE_USER_HEADER, DELETE_USER_TEXT, user=None, user_email=instance.email )

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save(update_fields=['is_deleted'])
		self.send_email(instance)

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
