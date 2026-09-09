from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('new/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
]