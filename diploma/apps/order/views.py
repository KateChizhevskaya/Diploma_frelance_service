from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser

from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.order.serializers import CreateOrderSerializer, UpdateOrderSerializer, RetrieveOrderSerializer, \
	ListOrderSerializer
from diploma.apps.utils.permissions import IsMasterPermission
from diploma.apps.verification.constants import BUFFER_PERIOD_USAGE
from diploma.apps.verification.models import VerificationClass


class CreateOrderView(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny, )
	serializer_class = CreateOrderSerializer


class PossibilityMixin:

	def get_existing_issue(self, email=None, phone=None):
		existing_code = None
		if phone and VerificationClass.objects.filter(phone=phone).exists():
			existing_code = VerificationClass.objects.get(phone=phone)
		elif VerificationClass.objects.filter(email=email).exists():
			existing_code = VerificationClass.objects.get(email=email)
		return existing_code

	def validate_verification(self, email=None, phone=None):
		existing_code = self.get_existing_issue(email, phone)
		if not existing_code:
			raise ValidationError(
				'You do not have any verification for that code/email'
			)
		if not existing_code.is_authorize:
			raise ValidationError(
				'You do not verify code'
			)
		if existing_code.authorizing_time + BUFFER_PERIOD_USAGE < timezone.now():
			existing_code.delete()
			raise ValidationError(
				'You validation is expired, please verify your email/phone once again'
			)

	def _validate_possibility(self, request, instance):
		email = request.data.get('customer_email')
		phone = request.data.get('customer_phone')
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
		) and not (
				instance.customer_email == email and instance.customer_email is not None
		):
			raise ValidationError(
				'You can not get that order'
			)
		self.validate_verification(email, phone)

	def remove_instance_after_changes(self, request):
		existing_instance = self.get_existing_issue(request.data.get('customer_email'), request.data.get('customer_phone'))
		existing_instance.delete()


class UpdateOrderView(generics.UpdateAPIView, PossibilityMixin):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				instance = WorkOrder.unapproved_objects.get(id=self.kwargs['id'])
				self._validate_possibility(self.request, instance)
				return instance
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not update that order'
			)

	def put(self, request, *args, **kwargs):
		result = super(UpdateOrderView, self).put(request, *args, **kwargs)
		if request.user.is_anonymous:
			self.remove_instance_after_changes(request)
		return result

	def patch(self, request, *args, **kwargs):
		result = super(UpdateOrderView, self).patch(request, *args, **kwargs)
		if request.user.is_anonymous:
			self.remove_instance_after_changes(request)
		return result


class RetrieveMyOrderView(generics.RetrieveAPIView, PossibilityMixin):
	permissions = (permissions.AllowAny, )
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
			try:
				instance = WorkOrder.objects.get(id=self.kwargs['id'])
			except WorkOrder.DoesNotExist:
				raise ValidationError(
					'You can not get that request'
				)
			self._validate_possibility(self.request, instance)
			return instance


class MyListOrderView(generics.ListAPIView, PossibilityMixin):
	permissions = (permissions.AllowAny, )
	serializer_class = ListOrderSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
	filterset_fields = ['status', ]
	ordering_fields = ['date_of_creating_request', 'date_time_of_work_begin']

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return WorkOrder.objects.filter(customer_email=self.request.user.email)
		else:
			email = self.request.data.get('customer_email')
			phone = self.request.data.get('customer_phone')
			if not phone and not email:
				raise ValidationError(
					'You have to provide phone or email to get list of orders'
				)
			self.validate_verification(email=email, phone=phone)
			if email:
				return WorkOrder.objects.filter(customer_email=email)
			else:
				return WorkOrder.objects.filter(customer_phone=phone)


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


class RemoveOrderView(generics.DestroyAPIView, PossibilityMixin):
	permission_classes = (permissions.AllowAny,)
	serializer_class = UpdateOrderSerializer

	def get_object(self):
		try:
			if not self.request.user.is_anonymous:
				return WorkOrder.unapproved_objects.get(id=self.kwargs['id'], customer_email=self.request.user.email)
			else:
				instance = WorkOrder.unapproved_objects.get(id=self.kwargs['id'], )
				self._validate_possibility(request=self.request, instance=instance)
				return instance
		except WorkOrder.DoesNotExist:
			raise ValidationError(
				'You can not remove that order'
			)

	def delete(self, request, *args, **kwargs):
		result = super(RemoveOrderView, self).delete(request, *args, **kwargs)
		if request.user.is_anonymous:
			self.remove_instance_after_changes(request)
		return result

