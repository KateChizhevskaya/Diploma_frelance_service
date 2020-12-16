from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from diploma.apps.permissions.permissions import IsMasterPermission
from diploma.apps.works.serializers import CreateWorkSerializer


class CreateWorkView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, IsMasterPermission, )
	serializer_class = CreateWorkSerializer