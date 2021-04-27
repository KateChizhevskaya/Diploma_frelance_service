from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from diploma.apps.verification.serializers import RequestForCodeSerializer


class RequestForCode(CreateAPIView):
	serializer_class = RequestForCodeSerializer
	permission_classes = (permissions.AllowAny,)
