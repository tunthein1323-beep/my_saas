from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'price_tier']

OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem, 
    fields=['product', 'quantity', 'unit_price'], 
    extra=8,  # Generates 8 initial empty product rows
    can_delete=False
)