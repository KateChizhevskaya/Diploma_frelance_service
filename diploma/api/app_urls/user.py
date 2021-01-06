from django.urls import path

from diploma.apps.user.views import ListUsersView, RetrieveUsersView, DeleteUserView

urlpatterns = [
	path('delete/<int:id>/', DeleteUserView.as_view(), name='user_delete'),
	path('<int:id>/', RetrieveUsersView.as_view(), name='user_retrieve'),
	path('', ListUsersView.as_view(), name='user_list'),
]
