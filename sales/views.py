from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Order
from .forms import OrderForm, OrderItemFormSet

def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.save()

                items = formset.save(commit=False)
                total = 0

                for item in items:
                    item.order = order
                    product = item.product

                    # Read pricing tier logic natively
                    if order.price_tier == 'distry':
                        item.unit_price = product.distry_price
                    elif order.price_tier == 'reseller':
                        item.unit_price = product.reseller_price
                    else:
                        item.unit_price = product.MSRP

                    # Deduct quantity from inventroy app instance
                    product.stock_quantity -= item.quantity
                    product.save()


                    item.save()
                    total += item.unit_price * item.quantity

                order.total_amount = total
                order.save()

            return redirect('sales:order_detail', order_id=order.id)
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'sales/create_order.html', {
        'order_form': order_form,
        'formset': formset
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'sales/order_detail.html', {'order': order})

def order_list(request):
    orders = Order.objects.all().order_by('-id')  # Fetches all orders, newest first
    return render(request, 'sales/order_list.html', {'orders': orders})