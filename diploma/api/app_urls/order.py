from django.urls import path

from diploma.apps.order.views import CreateOrderView, UpdateOrderView, RemoveOrderView, RetrieveOrderView, \
	ListOrderView, RetrieveMyOrderView, MyListOrderView

urlpatterns = [
	path('create/', CreateOrderView.as_view(), name='order_create'),
	path('update/<int:id>/', UpdateOrderView.as_view(), name='order_update'),
	path('remove/<int:id>/', RemoveOrderView.as_view(), name='order_remove'),
	path('my/<int:id>/', RetrieveMyOrderView.as_view(), name='my_order_retrieve'),
	path('my/', MyListOrderView.as_view(), name='my_order_list'),
	path('<int:id>/', RetrieveOrderView.as_view(), name='order_retrieve'),
	path('', ListOrderView.as_view(), name='order_list'),
]
