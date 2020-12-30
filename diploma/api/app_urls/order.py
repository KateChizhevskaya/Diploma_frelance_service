from django.urls import path

from diploma.apps.order.views import CreateOrderView, UpdateOrderView, RemoveOrderView, RetrieveOrderView, ListOrderView

urlpatterns = [
	path('create/', CreateOrderView.as_view(), name='order_create'),
	path('update/<int:id>/', UpdateOrderView.as_view(), name='order_update'),
	path('remove/<int:id>/', RemoveOrderView.as_view(), name='order_remove'),
	path('<int:id>/', RetrieveOrderView.as_view(), name='order_retrieve'),
	path('', ListOrderView.as_view(), name='order_list'),
]
