from django.urls import path
from .views import checkout, my_orders, order_detail, order_success

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
    path('success/<int:pk>/', order_success, name='order_success'),
]