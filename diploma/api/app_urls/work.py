from django.urls import path

from diploma.apps.works.views import CreateWorkView, WorkListView, WorkRetrieveView, WorkUpdateView, RemoveWorkView, \
	MyWorkListView, MyWorkRetrieveView

urlpatterns = [
	path('create/', CreateWorkView.as_view(), name='work_create'),
	path('update/<int:id>/', WorkUpdateView.as_view(), name='work_update'),
	path('delete/<int:id>/', RemoveWorkView.as_view(), name='work_remove'),
	path('my/<int:id>/', MyWorkRetrieveView.as_view(), name='my_work_retrieve'),
	path('my/', MyWorkListView.as_view(), name='my_works_list'),
	path('<int:id>/', WorkRetrieveView.as_view(), name='work_retrieve'),
	path('', WorkListView.as_view(), name='works_list'),
]
