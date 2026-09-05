from django import forms
from django.forms import inlineformset_factory
from .models import SalesOrder, SalesOrderLineItem  # Ensure correct models are imported

class SalesOrderForm(forms.ModelForm):
    class Meta:
        # --- THIS LINE WAS MISSING OR MISSPELLED ---
        model = SalesOrder  
        
        fields = [
            'customer', 'po_number', 'billing_address', 
            'shipping_address', 'expected_delivery', 
            'payment_term', 'sales_rep', 'tax_exempt'
        ]
        widgets = {
            'expected_delivery': forms.DateInput(attrs={'type': 'date'}),
        }

# Ensure your inline formset factory is configured correctly too
SalesOrderLineItemFormSet = inlineformset_factory(
    SalesOrder, 
    SalesOrderLineItem,
    fields=['product', 'description', 'quantity', 'unit_price'],
    extra=3,  
    can_delete=True
)