from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from app.models import Product, Customer # Import from your app models folder

def create_order(request):
    # FIXED: Context keys changed to match your HTML template loops
    inventory_list = Product.objects.all()
    customer_list = Customer.objects.all()

    return render(request, 'sales/create_order.html', {
        'inventory_list': inventory_list,
        'customer_list': customer_list,
    })

def get_product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # FIXED: JSON keys mapped to match data.part_number, data.description etc in JS
    return JsonResponse({
        'part_number': product.item_no,
        'description': product.description,
        'unit_price': str(product.MSRP),
        'available_stock': product.stock_quantity,
    })

def order_detail(request, order_id):
    from django.http import HttpResponse
    return HttpResponse(f"Viewing order details for ID: {order_id}")
