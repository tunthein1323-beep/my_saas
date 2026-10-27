from django.db import models

from django.contrib.auth.models import User

class Company(models.Model):
    c_name = models.CharField(max_length=50)
    c_phone = models.IntegerField()
    c_email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return f"{self.c_name} [{self. address}]"
    
class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.IntegerField(verbose_name="123456789")
    email = models.EmailField()    
    position = models.CharField(max_length=50, verbose_name="manager")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


#-----------------------------------Inventory------------------------------------
#class Category(models.Model):
   # name = models.CharField(max_length=100, unique=True)
   # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

   # class Meta:
    #    verbose_name_plural = "Categories"

   # def __str__(self):
     #   return self.name

class Product(models.Model):
    item_no = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    stock_quantity  = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    distry_price = models.DecimalField(max_digits=10, decimal_places=2)
    reseller_price = models.DecimalField(max_digits=10, decimal_places=2)
    MSRP = models.DecimalField(max_digits=10, decimal_places=2)
    dated_added = models.DateField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.item_no

        