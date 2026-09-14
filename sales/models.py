from django.db import models
from django.core.exceptions import ValidationError
from app.models import Customer, Product

class Order(models.Model):
    # FIXED: String syntax for app labels or direct model reference
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    billing_address = models.TextField(default='No Address Provided')
    # TYPO FIXED: changed 'shipping_adress' to 'shipping_address'
    shipping_address = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # REMOVED: Duplicate quantity field definition
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.product.sku
        if not self.description:
            # TYPO FIXED: changed 'self.prodcut' to 'self.product'
            self.description = self.product.description
        if not self.unit_price:
            self.unit_price = self.product.MSRP

        if not self.pk:
            if self.product.stock_quantity < self.quantity:
                raise ValidationError(f"Insufficient stock for {self.product.sku}.")
            
            self.product.stock_quantity -= self.quantity
            # BUG FIXED: Added parentheses to call the save method
            self.product.save()

        super().save(*args, **kwargs)
