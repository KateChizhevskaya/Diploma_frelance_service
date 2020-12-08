from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from diploma.apps.user.models import MasterUser
from diploma.apps.user.serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
	serializer_class = LoginSerializer
