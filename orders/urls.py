from django.urls import path
from .views import checkout, my_orders, order_detail

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
]