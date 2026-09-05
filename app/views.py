from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Customer, Product
from .forms import CompanyForm, CustomerForm, ProductForm

def home(request):
    return render(request, 'app/home.html')

#====================================Company name===================================
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'app/company_list.html', {'companies':companies})

def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
        # If the form is invalid, it falls through to render the errors
    else:
        form = CompanyForm() # Blank form for the initial GET request
    
    return render(request, 'app/company_form.html', {'form': form})

def company_update(request, pk):
    companies =get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=companies)
    if form.is_valid():
        form.save()
        return redirect('company_list')
    
    return render(request, 'app/company_form.html', {'form': form})

def company_delete(request, pk):
    companies = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        companies.delete()
        return redirect('company_list')
    return render(request, 'app/company_confirm_delete.html', {'companies': companies})


#====================================Customer Info===================================
def customer_list(request, company_id):
    # Fetch the specific company or return a 404 error if it doesn't exist
    company = get_object_or_404(Company, pk=company_id)
    
    # Get all customers belonging to this specific company
    customers = company.customers.all() 
    
    context = {
        'company': company,
        'customers': customers,
    }
    return render(request, 'app/customer_list.html', context)

def customer_create(request, company_id):

    # Fetch the company directly from the URL variable
    company = get_object_or_404(Company, pk=company_id)

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = company  # Automatically assign the customer to this company
            customer.save()
            return redirect('customer_list', company_id=company.id)
    else:
        form = CustomerForm()
    
    return render(request, 'app/customer_form.html', {
        'form': form, 
        'company': company  
    })

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # 🚨 FIX 1: Fetch the company belonging to this specific customer
    company = customer.company 

    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        # 🚨 FIX 2: Added the required company_id parameter to the redirect path
        return redirect('customer_list', company_id=company.id)
    
    return render(request, 'app/customer_form.html', {
        'form': form,
        'company': company,  # 🚨 FIX 3: Sent 'company' so the delete button displays!
        'customer': customer
    })

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # 🚨 FIX 4: Remember the company ID before deleting the customer record
    company_id = customer.company.id 
    
    if request.method == "POST":
        customer.delete()
        # 🚨 FIX 5: Use the saved company_id to safely return to the list view
        return redirect('customer_list', company_id=company_id)
    
    return render(request, 'app/customer_delete.html', {'customer': customer})

#====================================Inventory===================================
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products':products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        # If the form is invalid, it falls through to render the errors
    else:
        form = ProductForm() # Blank form for the initial GET request
    
    return render(request, 'inventory/product_form.html', {'form': form})

def product_update(request, pk):
    product =get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    
    else:
        # FIX: You MUST pass instance=product here to pre-populate the form with existing data
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {'form': form})

def product_delete(request, pk):
    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        products.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_delete.html', {'products': products})