from django.db import models
from django.utils import timezone
from decimal import Decimal

PAYMENT_TERM_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('net_15', 'Net 15'),
    ('net_30', 'Net 30'),
    ('net_45', 'Net 45'),
    ('net_60', 'Net 60'),
]

class SalesOrder(models.Model):
    # Main Order Metadata
    order_number = models.IntegerField(unique=True, editable=False)
    po_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="PO Number")
    customer = models.ForeignKey('app.Customer', on_delete=models.CASCADE, related_name='sales_orders')
    
    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True)
    
    order_date = models.DateField(default=timezone.now)
    expected_delivery = models.DateField()  
    
    payment_term = models.CharField(max_length=20, choices=PAYMENT_TERM_CHOICES, default='net_30')
    sales_rep = models.CharField(max_length=100)
    tax_exempt = models.BooleanField(default=False, verbose_name="Tax Exempt")

    # Calculations for multiple products across the order
    @property
    def subtotal(self):
        # Uses sum() to loop through all connected SalesOrderLineItem entries
        return sum(item.amount for item in self.items.all())
    
    @property
    def tax_amount(self):
        if self.tax_exempt:
            return Decimal('0.00')
        return round(self.subtotal * Decimal('0.0725'), 2)
    
    @property
    def grand_total(self):
        return self.subtotal + self.tax_amount

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = SalesOrder.objects.order_by('-order_number').first()
            self.order_number = last_order.order_number + 1 if last_order else 10001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SO-{self.order_number}"


class SalesOrderLineItem(models.Model):
    # Links each specific line item row back to its parent SalesOrder container
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    
    # Selected product, specific quantities, and explicit pricing boundaries
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='order_items')
    description= models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def amount(self):
        # Calculation formula logic isolated per product row line
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.item_no} (Qty: {self.quantity})"