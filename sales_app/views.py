from django.shortcuts import render, redirect
from .forms import SalesOrderForm, SalesOrderLineItemFormSet
from .models import SalesOrder, SalesOrderLineItem

def order_success(request):
    """Renders the final order registration confirmation message view template."""
    return render(request, 'sales/order_success.html')

def create_sales_order(request):
    if request.method == "POST":
        form = SalesOrderForm(request.POST)

        if form.is_valid():
            sales_order = form.save()

            formset = SalesOrderLineItemFormSet(request.POST, instance=sales_order)
            if formset.is_valid():
                formset.save()
                return redirect('order_success_page')
            
    else:
        form = SalesOrderForm()
        formset = SalesOrderLineItemFormSet()

    return render(request, 'sales/order_form.html', {
        'form': form,
        'formset': formset
    })
