from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('commit/', views.commit, name='commit'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('success/<int:pk>/', views.order_success, name='order_success'),
    path('payment-failed/<int:pk>/', views.payment_failed, name='payment_failed'),
]