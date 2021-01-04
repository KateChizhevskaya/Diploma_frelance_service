from rest_framework import generics, permissions

from diploma.apps.black_list.constants import BLACK_LIST_HEADER, BLACK_LIST_REMOVE_TEXT
from diploma.apps.black_list.models import BlackList
from diploma.apps.black_list.serializers import CreateBlackListNoteViewSerializer, RemoveBlackListNoteSerializer
from diploma.apps.tasks.mail_sending import send_email


class CreateBlackListNoteView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = CreateBlackListNoteViewSerializer


class RemoveBlackListNoteView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	lookup_field = 'id'
	serializer_class = RemoveBlackListNoteSerializer
	queryset = BlackList.objects.all()

	def send_email(self, instance):
		if instance.email:
			send_email(BLACK_LIST_HEADER, BLACK_LIST_REMOVE_TEXT, user=None, user_email=instance.email)

	def perform_destroy(self, instance):
		super(RemoveBlackListNoteView, self).perform_destroy(instance)
		self.send_email(instance)