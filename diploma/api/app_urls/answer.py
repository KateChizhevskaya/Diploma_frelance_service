from django.urls import path

from diploma.apps.answers.views import CreateOrderAnswerView, MyCreatedOrderListView, CreateOrderMyAnsweredListView, \
	CreateComplaintAnswerView, AnswersToMyComplaintListView, MyAnsweredComplaintListView

urlpatterns = [
	path('create_order_answer/', CreateOrderAnswerView.as_view(), name='order_answer_create'),
	path('my_orders_answer/', MyCreatedOrderListView.as_view(), name='my_orders_answer'),
	path('answered_by_me_orders/', CreateOrderMyAnsweredListView.as_view(), name='answered_by_me_orders'),
	path('create_complaint_answer/', CreateComplaintAnswerView.as_view(), name='complaint_answer_create'),
	path('my_complaints_answer/', AnswersToMyComplaintListView.as_view(), name='my_complaints_answer'),
	path('answered_by_me_complaints/', MyAnsweredComplaintListView.as_view(), name='answered_by_me_complaints'),
]
