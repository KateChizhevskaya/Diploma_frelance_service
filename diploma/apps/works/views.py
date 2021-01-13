from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.order.constants import ACTIVE_STATUS
from diploma.apps.order.models import WorkOrder
from diploma.apps.tasks.mail_sending import send_mails_to_many_users
from diploma.apps.utils.filters import WorkFilter
from diploma.apps.utils.permissions import IsMasterPermission
from diploma.apps.works.constants import WORK_TEXT_START, WORK_DELETE_TEXT_END, WORK_DELETE_HEADER
from diploma.apps.works.models import Work
from diploma.apps.works.serializers import CreateWorkSerializer, ListWorkSerializer, UpdateWorkSerializer, \
	RetrieveWorkSerializer


class CreateWorkView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateWorkSerializer


class WorkListView(generics.ListAPIView):
	permission_classes = (permissions.AllowAny, )
	serializer_class = ListWorkSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = WorkFilter
	queryset = Work.active_objects.all()
	search_fields = ['name', ]


class WorkRetrieveView(generics.RetrieveAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = RetrieveWorkSerializer
	lookup_field = 'id'
	queryset = Work.active_objects.all()


class MyWorkListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission,)
	serializer_class = ListWorkSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = WorkFilter
	search_fields = ['name', ]

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return Work.active_objects.filter(worker=self.request.user)
		else:
			raise ValidationError(
				'You need to log in'
			)


class MyWorkRetrieveView(generics.RetrieveAPIView):
	serializer_class = RetrieveWorkSerializer
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission,)
	lookup_field = 'id'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return Work.active_objects.filter(worker=self.request.user)
		else:
			raise ValidationError(
				'You need to log in'
			)


class WorkUpdateView(generics.UpdateAPIView):
	serializer_class = UpdateWorkSerializer
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )

	def get_object(self):
		if self.request.user.is_authenticated:
			try:
				return Work.active_objects.get(id=self.kwargs['id'], worker=self.request.user)
			except Work.DoesNotExist:
				raise ValidationError(
					'You can not update that work'
				)
		else:
			raise ValidationError(
				'You need to log in'
			)


class RemoveWorkView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission,)

	def get_object(self):
		if self.request.user.is_authenticated:
			try:
				return Work.active_objects.get(id=self.kwargs['id'], worker=self.request.user)
			except Work.DoesNotExist:
				raise ValidationError(
					'You can not delete that work'
				)
		else:
			raise ValidationError(
				'You need to log in'
			)

	def send_email(self, instance):
		text = WORK_TEXT_START + instance.name + WORK_DELETE_TEXT_END
		emails = filter(
			lambda one_order: one_order is not None,
			(order.customer_email for order in WorkOrder.objects.filter(work__id=instance.id, status__in=ACTIVE_STATUS))
		)
		send_mails_to_many_users(WORK_DELETE_HEADER, text, users=None, users_mails=emails)

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save(update_fields=['is_deleted'])
		self.send_email(instance)

