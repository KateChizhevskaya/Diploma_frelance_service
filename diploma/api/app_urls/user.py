from django.urls import path

from diploma.apps.user.views import ListUsersView, RetrieveUsersView, DeleteUserView, UpdateUserView, AdminUpdateUser

urlpatterns = [
	path('delete/<int:id>/', DeleteUserView.as_view(), name='user_delete'),
	path('admin_update/<int:id>/', AdminUpdateUser.as_view(), name='user_admin_update'),
	path('update/', UpdateUserView.as_view(), name='user_itself_update'),
	path('<int:id>/', RetrieveUsersView.as_view(), name='user_retrieve'),
	path('', ListUsersView.as_view(), name='user_list'),
]
