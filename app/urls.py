from django.urls import path
from . import views

# Make sure these are square brackets [ ] and NOT curly braces { }
urlpatterns = [
    path('', views.home, name='home'),
    path('company/', views.company_list, name='company_list'),
    path('new/', views.company_create, name='company_create'),
    path('edit/<int:pk>/', views.company_update, name='company_update'),
    path('delete/<int:pk>/', views.company_delete, name='company_delete'),

   path('company/<int:company_id>/customers/', views.customer_list, name='customer_list'),
    
    # 2. Add a new customer directly under a specific company
    path('company/<int:company_id>/customer/add/', views.customer_create, name='customer_create'),
    
    # 3. Update an existing customer record
    path('customer/edit/<int:pk>/', views.customer_update, name='customer_update'),
    
    # 4. Remove an existing customer record
    path('customer/delete/<int:pk>/', views.customer_delete, name='customer_delete'),

    path('product/', views.product_list, name='product_list'),
    path('product_new/', views.product_create, name='product_create'),
    path('product_edit/<int:pk>/', views.product_update, name='product_update'),
    path('product_delete/<int:pk>/', views.product_delete, name='product_delete'),
]