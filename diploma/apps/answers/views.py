from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.answers.models import OrderAnswer, ComplaintAnswer
from diploma.apps.answers.serializers import CreateOrderAnswerSerializer, CreateComplaintAnswerSerializer
from diploma.apps.utils.permissions import IsMasterPermission


class CreateOrderAnswerView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateOrderAnswerSerializer


class CreateComplaintAnswerView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = CreateComplaintAnswerSerializer


class MyAnsweredComplaintListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = CreateComplaintAnswerSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return ComplaintAnswer.objects.filter(answered_admin=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class AnswersToMyComplaintListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = CreateComplaintAnswerSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return ComplaintAnswer.objects.filter(complaint__complaint_creater=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class MyCreatedOrderListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = CreateOrderAnswerSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return OrderAnswer.objects.filter(order__customer_email=self.request.user.email)
		else:
			raise ValidationError(
				'You need to login first'
			)


class CreateOrderMyAnsweredListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateOrderAnswerSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return OrderAnswer.objects.filter(order__work__worker=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)
