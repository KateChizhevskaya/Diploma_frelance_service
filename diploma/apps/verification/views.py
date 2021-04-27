from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from diploma.apps.verification.serializers import RequestForCodeSerializer, VerifyCodeSerializer


class RequestForCode(CreateAPIView):
	serializer_class = RequestForCodeSerializer
	permission_classes = (permissions.AllowAny,)


class VerifyCode(CreateAPIView):
	serializer_class = VerifyCodeSerializer
	permission_classes = (permissions.AllowAny,)
