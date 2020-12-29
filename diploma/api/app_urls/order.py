from django.urls import path

from diploma.apps.order.views import CreateOrderView, UpdateOrderView

urlpatterns = [
	path('create/', CreateOrderView.as_view(), name='order_create'),
	path('update/<int:id>/', UpdateOrderView.as_view(), name='order_update'),
]
