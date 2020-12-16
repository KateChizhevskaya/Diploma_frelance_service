from django.urls import path

from diploma.apps.works.views import CreateWorkView

urlpatterns = [
	path('create/', CreateWorkView.as_view(), name='create_work'),
]