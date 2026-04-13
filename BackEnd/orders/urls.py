from django.urls import path
from .views import OrderListView, OrderCancelView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]
