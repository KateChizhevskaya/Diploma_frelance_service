from django.urls import path

from diploma.apps.works.views import CreateWorkView, WorkListView, WorkRetrieveView, WorkUpdateView

urlpatterns = [
	path('create/', CreateWorkView.as_view(), name='create_work'),
	path('update/<int:id>/', WorkUpdateView.as_view(), name='work_update'),
	path('<int:id>/', WorkRetrieveView.as_view(), name='work_retrieve'),
	path('', WorkListView.as_view(), name='works_list'),
]