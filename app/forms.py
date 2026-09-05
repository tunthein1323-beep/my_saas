from django import forms
from .models import Company, Customer, Product


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company  # 2. This line fixes the ValueError!
        fields = ['c_name', 'c_phone', 'c_email', 'address']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer  # 2. This line fixes the ValueError!
        fields = ['first_name', 'last_name', 'phone', 'email', 'position']

#----------------------------inventory----------------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # 2. This line fixes the ValueError!
        fields = ['item_no', 'sku', 'description', 'stock_quantity', 'cost_price',
                  'distry_price', 'reseller_price', 'MSRP']
