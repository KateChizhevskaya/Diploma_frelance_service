from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.answers.models import OrderAnswer
from diploma.apps.answers.serializers import CreateOrderAnswerSerializer
from diploma.apps.utils.permissions import IsMasterPermission


class CreateOrderAnswerView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateOrderAnswerSerializer


class MyCreatedOrderListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = CreateOrderAnswerSerializer

	def get_queryset(self):
		return OrderAnswer.objects.filter(order__customer_email=self.request.user.email)


class CreateOrderMyAnsweredListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateOrderAnswerSerializer

	def get_queryset(self):
		return OrderAnswer.objects.filter(order__work__worker=self.request.user)
