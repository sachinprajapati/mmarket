from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
User = get_user_model()

from products.models import *

# Create your views here.
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
def allProducts(request):
	return render(request, 'products-list.html')

def addProducts(request):
	return render(request, 'add-products.html')

def editProducts(request):
	return render(request, 'edit-products.html')
# Categories

@method_decorator(staff_member_required, name='dispatch')
class AllCategories(ListView):
	queryset = Category.objects.all()
	template_name = 'categories-list.html'
	context_object_name = 'category_list'

@method_decorator(staff_member_required, name='dispatch')
class UpdateCategory(UpdateView):
	template_name = "form_view.html"
	model = Category
	fields = "__all__"
	success_url = reverse_lazy('update_category')

def addCategories(request):
	return render(request, 'add-categories.html')

def editCategories(request):
	return render(request, 'edit-categories.html')
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
