from django.urls import path
from . import views

urlpatterns = [
    
    # NEW: The Sales Order Workspace Page (Accessible at /sales_app/order/create/)
    path('order/create/', views.create_sales_order, name='create_sales_order'),
    
    # NEW: The Success Page Redirect Destination (Accessible at /sales_app/order/success/)
    path('order/success/', views.order_success, name='order_success_page'),
]