from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter


class CreateWorkView(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny, )
	serializer_class = CreateOrderSerializer