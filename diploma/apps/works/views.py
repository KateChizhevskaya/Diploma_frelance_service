from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.utils.filters import WorkFilter
from diploma.apps.utils.permissions import IsMasterPermission
from diploma.apps.works.constants import WORK_TEXT_START, WORK_DELETE_TEXT_END
from diploma.apps.works.models import Work
from diploma.apps.works.serializers import CreateWorkSerializer, ListRetrieveWorkSerializer, UpdateWorkSerializer


class CreateWorkView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateWorkSerializer


class WorkListView(generics.ListAPIView):
	serializer_class = ListRetrieveWorkSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = WorkFilter
	queryset = Work.active_objects.all()
	search_fields = ['name', ]


class WorkRetrieveView(generics.RetrieveAPIView):
	serializer_class = ListRetrieveWorkSerializer
	lookup_field = 'id'
	queryset = Work.active_objects.all()


class WorkUpdateView(generics.UpdateAPIView):
	serializer_class = UpdateWorkSerializer
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )

	def get_object(self):
		try:
			return Work.active_objects.get(id=self.kwargs['id'], worker=self.request.user)
		except Work.DoesNotExist:
			raise ValidationError(
				'You can not update that work'
			)


class RemoveWorkView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission,)

	def get_object(self):
		try:
			return Work.active_objects.get(id=self.kwargs['id'], worker=self.request.user)
		except Work.DoesNotExist:
			raise ValidationError(
				'You can not delete that work'
			)

	def send_email(self, instance):
		text = WORK_TEXT_START + instance.name + WORK_DELETE_TEXT_END
		# sending emails for all who have active or not approved requests for job

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save(update_fields=['is_deleted'])
		self.send_email(instance)

