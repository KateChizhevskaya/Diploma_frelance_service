from django.urls import path

from diploma.apps.reactions.views import AddReviewView, UpdateReviewView

urlpatterns = [
	path('review/create/', AddReviewView.as_view(), name='review_create'),
	path('review/<int:id>/', UpdateReviewView.as_view(), name='review_update_destroy'),
]
