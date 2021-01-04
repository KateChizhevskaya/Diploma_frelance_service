from django.urls import path

from diploma.apps.black_list.views import CreateBlackListNoteView, RemoveBlackListNoteView

urlpatterns = [
	path('create/', CreateBlackListNoteView.as_view(), name='black_list_create'),
	path('delete/<int:id>/', RemoveBlackListNoteView.as_view(), name='black_list_remove_remove'),
]
