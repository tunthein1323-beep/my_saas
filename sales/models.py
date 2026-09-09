from django.db import models

from app.models import Customer, Product

class Order(models.Model):
    PRICE_CHOICES = [
        ('distry', 'Distributor Price'),
        ('reseller', 'Reseller Price'),
        ('msrp', 'MSRP'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order')
    price_tier = models.CharField(max_length=10, choices=PRICE_CHOICES, default='msrp')
    created_at = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.item_no} for Order #{self.order.id}"