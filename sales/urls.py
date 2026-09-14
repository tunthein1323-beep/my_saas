from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # 1. Create Order Page
    path('create-order/', views.create_order, name='create_order'),
    
    # 2. Saved Orders History List (ADDED THIS LINE)
    path('orders/', views.sales_orders_list, name='sales_orders_list'),
    
    # CRITICAL: This pattern must match your fetch path precisely!
    path('api/product/<int:product_id>/', views.get_product_detail, name='get_product_detail'),
    
    # 3. Individual Order Detail view
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
