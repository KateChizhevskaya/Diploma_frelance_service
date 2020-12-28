from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from diploma.apps.utils.filters import WorkFilter
from diploma.apps.utils.permissions import IsMasterPermission
from diploma.apps.works.models import Work
from diploma.apps.works.serializers import CreateWorkSerializer, ListRetrieveWorkSerializer, UpdateWorkSerializer


class CreateWorkView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateWorkSerializer


class WorkListView(generics.ListAPIView):
	serializer_class = ListRetrieveWorkSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = WorkFilter
	queryset = Work.objects.filter(worker__is_deleted=False)
	search_fields = ['name', ]


class WorkRetrieveView(generics.RetrieveAPIView):
	serializer_class = ListRetrieveWorkSerializer
	lookup_field = 'id'
	queryset = Work.objects.filter(worker__is_deleted=False)


class WorkUpdateView(generics.UpdateAPIView):
	serializer_class = UpdateWorkSerializer
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )

	def get_object(self):
		try:
			return Work.objects.get(id=self.kwargs['id'], worker=self.request.user, worker__is_deleted=False)
		except Work.DoesNotExist:
			raise ValidationError(
				'You can update that work'
			)
