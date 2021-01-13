from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter

from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.order.serializers import CreateOrderSerializer, UpdateOrderSerializer, RetrieveOrderSerializer, \
	ListOrderSerializer
from diploma.apps.utils.permissions import IsMasterPermission


class CreateOrderView(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny, )
	serializer_class = CreateOrderSerializer


class UpdateOrderView(generics.UpdateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def _validate_possibility(self, instance):
		email = self.request.data.get('email')
		phone = self.request.data.get('phone')
		if instance.status != Statuses.IN_PROCESS:
			raise ValidationError(
				'You can not update answered order'
			)
		if not phone and not email:
			raise ValidationError(
				'You have to provide customer_phone or customer_email to update that order'
			)
		elif not (
				instance.customer_phone == phone and instance.customer_phone is not None
		) or not (
				instance.customer_email == email and instance.customer_email is not None
		):
			raise ValidationError(
				'You can not update that order'
			)

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				instance = WorkOrder.unapproved_objects.get(id=self.kwargs['id'])
				self._validate_possibility(instance)
				return instance
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not update that order'
			)


class RetrieveOrderView(generics.RetrieveAPIView):
	permissions = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = RetrieveOrderSerializer

	def get_object(self):
		if not self.request.user.is_anonymous:
			try:
				return WorkOrder.objects.get(id=self.kwargs['id'], work__worker=self.request.user)
			except WorkOrder.DoesNotExist:
				raise ValidationError(
					'You can not get that request'
				)
		else:
			raise ValidationError(
				'You need to login first'
			)


class ListOrderView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = ListOrderSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
	filterset_fields = ['status', ]
	ordering_fields = ['date_of_creating_request', 'date_time_of_work_begin']

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return WorkOrder.objects.filter(work__worker=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class MyListOrderView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, )
	serializer_class = ListOrderSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
	filterset_fields = ['status', ]
	ordering_fields = ['date_of_creating_request', 'date_time_of_work_begin']

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return WorkOrder.objects.filter(customer_email=self.request.user.email)
		else:
			raise ValidationError(
				'You need to login first'
			)


class RetrieveMyOrderView(generics.RetrieveAPIView):
	permissions = (permissions.IsAuthenticated, )
	serializer_class = RetrieveOrderSerializer

	def get_object(self):
		if not self.request.user.is_anonymous:
			try:
				return WorkOrder.objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			except WorkOrder.DoesNotExist:
				raise ValidationError(
					'You can not get that request'
				)
		else:
			raise ValidationError(
				'You need to login first'
			)


class RemoveOrderView(generics.DestroyAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def _validate_possibility(self, instance):
		email = self.request.data.get('email')
		phone = self.request.data.get('phone')
		if not phone and not email:
			raise ValidationError(
				'You have to provide customer_phone or customer_email to delete order'
			)
		elif not (
				instance.customer_phone == phone and instance.customer_phone is not None
		) or not (
				instance.customer_email == email and instance.customer_email is not None
		):
			raise ValidationError(
				'You can not delete that order'
			)

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				instance = WorkOrder.unapproved_objects.get(id=self.kwargs['id'], )
				self._validate_possibility(instance)
				return instance
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not remove that order'
			)
