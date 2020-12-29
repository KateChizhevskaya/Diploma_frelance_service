from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.order.serializers import CreateOrderSerializer, UpdateOrderSerializer


class CreateOrderView(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny, )
	serializer_class = CreateOrderSerializer


class UpdateOrderView(generics.UpdateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'])
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not update that order'
			)


class RemoveOrderView(generics.DestroyAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'])
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not remove that order'
			)