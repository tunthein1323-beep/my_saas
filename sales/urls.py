# In your sales/urls.py file
from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    
    # CRITICAL: This pattern must match your fetch path precisely!
    path('api/product/<int:product_id>/', views.get_product_detail, name='get_product_detail'),
    
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
