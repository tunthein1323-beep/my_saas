from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from app.models import Product, Customer
from .models import Order, OrderItem

def create_order(request):
    """
    Handles both rendering the empty order form (GET) and processing 
    the complex mathematical order calculations to save to the database (POST).
    """
    if request.method == "POST":
        # Log exactly what data is arriving in your terminal console
        print("DEBUG POST DATA:", request.POST) 

        customer_id = request.POST.get('customer_id')
        
        # If customer_id is missing or is just an empty string ''
        if not customer_id or customer_id.strip() == "":
            return HttpResponseBadRequest("Customer is required. Received an empty value.")

        
        customer = get_object_or_404(Customer, pk=customer_id)
        billing_address = request.POST.get('billing_address', 'No Address Provided')
        shipping_address = request.POST.get('shipping_address', '')

        # Grab arrays of dynamically submitted rows from your HTML form input fields
        product_ids = request.POST.getlist('product_ids')
        quantities = request.POST.getlist('quantities')

        try:
            # Wrap the database writes in an atomic transaction blocks.
            # If one item fails (e.g. out of stock), nothing gets half-saved.
            with transaction.atomic():
                # 1. Initialize and save the parent Order record
                order = Order.objects.create(
                    customer=customer,
                    billing_address=billing_address,
                    shipping_address=shipping_address
                )

                running_sub_total = Decimal('0.00')

                # 2. Iterate through each product row submitted from the frontend
                for p_id, qty_str in zip(product_ids, quantities):
                    if not p_id or not qty_str:
                        continue
                        
                    product = get_object_or_404(Product, pk=p_id)
                    quantity = int(qty_str)
                    
                    # Convert MSRP to Decimal for exact bank-safe calculation
                    unit_price = Decimal(str(product.MSRP or 0))
                    amount = quantity * unit_price
                    running_sub_total += amount

                    # 3. Create individual OrderItem. 
                    # This automatically triggers stock reductions in your model's save().
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        amount=amount
                    )

                # 4. Process overarching financial metrics
                tax_rate = Decimal('0.0725') # 7.25% Tax rate
                tax_total = running_sub_total * tax_rate
                grand_total = running_sub_total + tax_total

                # 5. Populate and update the calculations into the parent Order entry
                order.sub_total = round(running_sub_total, 2)
                order.tax = round(tax_total, 2)
                order.total = round(grand_total, 2)
                order.save()

            return redirect('sales:sales_orders_list')

        except ValidationError as e:
            # Gracefully handle validation errors (like out-of-stock messages) back to the form
            inventory_list = Product.objects.all()
            customer_list = Customer.objects.all()
            return render(request, 'sales/create_order.html', {
                'inventory_list': inventory_list,
                'customer_list': customer_list,
                'error_message': e.message,
            })

    # Standard empty GET Request layout instantiation
    inventory_list = Product.objects.all()
    customer_list = Customer.objects.all()
    return render(request, 'sales/create_order.html', {
        'inventory_list': inventory_list,
        'customer_list': customer_list,
    })


def sales_orders_list(request):
    """
    Queries all completed records from the database and returns them 
    sorted from newest to oldest for your summary interface screen.
    """
    orders = Order.objects.all().order_by('-id')
    return render(request, 'sales/sales_orders_list.html', {
        'orders': orders
    })


def get_product_detail(request, product_id):
    """
    API Endpoint returning product meta specifications via JSON.
    Allows JavaScript on your Mac's browser to read live updates.
    """
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse({
        'part_number': product.item_no,
        'description': product.description,
        'unit_price': str(product.MSRP),
        'available_stock': product.stock_quantity,
    })


def order_detail(request, order_id):
    """
    Dynamic path viewing fallback placeholder for single orders.
    """
    from django.http import HttpResponse
    return HttpResponse(f"Viewing order details for ID: {order_id}")
