from django.urls import path

from diploma.apps.reactions.views import AddReviewView, UpdateDeleteReviewView, AddComplaintView, ListComplaintView, \
	RetrieveComplaintView

urlpatterns = [
	path('review/create/', AddReviewView.as_view(), name='review_create'),
	path('review/<int:id>/', UpdateDeleteReviewView.as_view(), name='review_update_destroy'),
	path('complaint/create/', AddComplaintView.as_view(), name='complaint_create'),
	path('complaint/<int:id>/', RetrieveComplaintView.as_view(), name='complaint_retrieve'),
	path('complaint/', ListComplaintView.as_view(), name='complaint_list'),
]
