from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django_tables2 import SingleTableView

from django.contrib.auth import get_user_model
User = get_user_model()

from products.models import *
from .tables import *

# Create your views here.
@staff_member_required(login_url=reverse_lazy('login'))
def index(request):
	if request.user.is_staff:
		return render(request, 'index.html')
	return render(request, 'index.html')

def notFound(request):
	return render(request, '404.html')
# Customers
class Customers(ListView):
	template_name = 'customers.html'
	queryset = User.objects.filter(is_staff=False, is_superuser=False)


def editCustomers(request):
	return render(request, 'edit-customer.html')

# Products
@method_decorator(staff_member_required, name='dispatch')
class AllProducts(SingleTableView):
	queryset = Product.objects.filter()
	template_name = 'categories-list.html'
	table_class = ProductTable

@method_decorator(staff_member_required, name='dispatch')
class AddProducts(SuccessMessageMixin, CreateView):
	model = Product
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('products_list')
	success_message = "%(name)s successfully created"

class UpdateProducts(SuccessMessageMixin, UpdateView):
	model = Product
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('products_list')
	success_message = "%(name)s successfully updated"


# Products
@method_decorator(staff_member_required, name='dispatch')
class AllProductClass(SingleTableView):
	queryset = ProductClass.objects.filter()
	template_name = 'categories-list.html'
	table_class = ProductCLassTable

@method_decorator(staff_member_required, name='dispatch')
class AddProductClass(SuccessMessageMixin, CreateView):
	model = ProductClass
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('product_class_list')
	success_message = "%(name)s successfully created"

class UpdateProductClass(SuccessMessageMixin, UpdateView):
	model = ProductClass
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('product_class_list')
	success_message = "%(name)s successfully updated"

# Categories

@method_decorator(staff_member_required, name='dispatch')
class AllCategories(SingleTableView):
	queryset = Category.objects.all()
	template_name = 'categories-list.html'
	table_class = CategoryTable
	table_pagination = False

@method_decorator(staff_member_required, name='dispatch')
class UpdateCategory(SuccessMessageMixin, UpdateView):
	template_name = "form_view.html"
	model = Category
	fields = "__all__"
	success_message = "%(name)s successfully updated"
	success_url = reverse_lazy('categories-list')

class AddCategories(SuccessMessageMixin, CreateView):
	model = Category
	fields = ("name", "parent", "img")
	template_name = "form_view.html"
	success_url = reverse_lazy('categories-list')
	success_message = "%(name)s successfully created"

def editCategories(request):
	return render(request, 'edit-categories.html')

@method_decorator(staff_member_required, name='dispatch')
class DeleteCategory(DeleteView):
	model = Category
	success_url = reverse_lazy('categories-list')

@method_decorator(staff_member_required, name='dispatch')
class AddProductsImages(SuccessMessageMixin, CreateView):
	model = ProductImage
	template_name = "form_view.html"
	fields = "__all__"
	success_url = reverse_lazy('products_list')
	success_message = "Product Image Successfully Added"

# Banners
def allBanner(request):
	return render(request, 'banners-list.html')

def addBanner(request):
	return render(request, 'add-banner.html')

def editBanner(request):
	return render(request, 'edit-banner.html')
# Orders
def confirmedOrders(request):
	return render(request, 'confirmed-orders.html')

def packedOrders(request):
	return render(request, 'packed-orders.html')

def outfordeliveredOrders(request):
	return render(request, 'out-for-delivered-orders.html')

def deliveredOrders(request):
	return render(request, 'delivered-orders.html')

def rejectedOrders(request):
	return render(request, 'rejected-orders.html')
