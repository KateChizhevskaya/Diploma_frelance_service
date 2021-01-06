from django.urls import path

from diploma.apps.reactions.views import AddReviewView, UpdateDeleteReviewView, AddComplaintView, ListComplaintView, \
	RetrieveComplaintView, ListMyReviewsView, RetrieveMyReviewView

urlpatterns = [
	path('review/create/', AddReviewView.as_view(), name='review_create'),
	path('review/<int:id>/', UpdateDeleteReviewView.as_view(), name='review_update_destroy'),
	path('complaint/create/', AddComplaintView.as_view(), name='complaint_create'),
	path('complaint/<int:id>/', RetrieveComplaintView.as_view(), name='complaint_retrieve'),
	path('complaint/', ListComplaintView.as_view(), name='complaint_list'),
	path('my_complaint/<int:id>/', RetrieveComplaintView.as_view(), name='my_complaint_retrieve'),
	path('my_complaint/', ListComplaintView.as_view(), name='my_complaint_list'),
	path('my_review/<int:id>/', RetrieveMyReviewView.as_view(), name='my_review_retrieve'),
	path('my_review/', ListMyReviewsView.as_view(), name='my_review_list'),
]
