from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.forms import modelformset_factory

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView

from django.contrib.auth import get_user_model
User = get_user_model()

from products.models import *
from orders.models import *
from .tables import *
from .forms import *
from .models import *

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
@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AllProducts(SingleTableView):
	queryset = Product.objects.filter()
	template_name = 'list_view.html'
	table_class = ProductTable

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddProducts(SuccessMessageMixin, CreateView):
	form_class = AddProduct
	template_name = "form_view.html"
	success_url = reverse_lazy('products_list')
	success_message = "%(name)s successfully created"

	def get_success_url(self):
		return reverse_lazy('add_product_images', args=(self.object.id,))

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateProducts(SuccessMessageMixin, UpdateView):
	form_class = AddProduct
	template_name = "form_view.html"
	success_url = reverse_lazy('products_list')
	success_message = "%(name)s successfully updated"

	def get_object(self):
		return Product.objects.get(pk=self.kwargs.get('pk'))

	def get_success_url(self):
		return reverse_lazy('add_product_images', args=(self.object.id,))


# Products
@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AllProductClass(SingleTableView):
	queryset = ProductClass.objects.filter()
	template_name = 'list_view.html'
	table_class = ProductCLassTable

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddProductClass(SuccessMessageMixin, CreateView):
	model = ProductClass
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('product_class_list')
	success_message = "%(name)s successfully created"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateProductClass(SuccessMessageMixin, UpdateView):
	model = ProductClass
	fields = "__all__"
	template_name = "form_view.html"
	success_url = reverse_lazy('product_class_list')
	success_message = "%(name)s successfully updated"

# Categories

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AllCategories(SingleTableView):
	queryset = Category.objects.all()
	template_name = 'list_view.html'
	table_class = CategoryTable
	table_pagination = False

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateCategory(SuccessMessageMixin, UpdateView):
	template_name = "form_view.html"
	model = Category
	fields = "__all__"
	success_message = "%(name)s successfully updated"
	success_url = reverse_lazy('categories-list')

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddCategories(SuccessMessageMixin, CreateView):
	model = Category
	fields = ("name", "parent", "img")
	template_name = "form_view.html"
	success_url = reverse_lazy('categories-list')
	success_message = "%(name)s successfully created"

def editCategories(request):
	return render(request, 'edit-categories.html')

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DeleteCategory(DeleteView):
	model = Category
	success_url = reverse_lazy('categories-list')

# @method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
# class AddProductsImages(SuccessMessageMixin, CreateView):
# 	model = ProductImage
# 	template_name = "product_images.html"
# 	fields = "__all__"
# 	success_url = reverse_lazy('products_list')
# 	success_message = "Product Image Successfully Added"
#
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
# 		return context


@staff_member_required(login_url=reverse_lazy('login'))
def AddProductsImages(request, pk):
	template_name = 'product_images.html'
	product = get_object_or_404(Product, pk=pk)
	ProductImageFormset = modelformset_factory(ProductImage, exclude=("product",), extra=6-product.images.all().count(), min_num=1,
													 form=AddProductImage, can_delete=True)
	formset = ProductImageFormset(request.POST or None, request.FILES or None, queryset=ProductImage.objects.filter(product=product))
	if request.method == "POST":
		if formset.is_valid():
			for form in formset:
				instance = form.save(commit=False)
				instance.product = product
			formset.save()
			messages.success(request, 'product images successfully updated')
			return redirect(reverse_lazy('products_list'))
	return render(request, template_name, {
		'formset': formset,
		'product': product,
	})


@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateOrders(SuccessMessageMixin, UpdateView):
	template_name = "form_view.html"
	form_class = OrderStatusForm
	success_message = "%(name)s successfully updated"
	success_url = reverse_lazy('categories-list')

	def get_object(self):
		return Orders.objects.get(pk=self.kwargs.get('pk'))

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AllOrders(SingleTableMixin, FilterView):
	table_class = OrdersTable
	model = Orders
	template_name = "list_view.html"
	filterset_class = OrdersFilter
	queryset = model.objects.filter()


@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DetailOrders(DetailView):
	model = Orders
	context_object_name = 'order'
	template_name = "orders_detail.html"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DetailCustomer(DetailView):
	model = User
	context_object_name = 'customer'
	template_name = "customer_detail.html"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class ListCustomer(SingleTableMixin, FilterView):
	table_class = UserList
	model = User
	template_name = "list_view.html"
	filterset_class = UsersFilter
	queryset = model.objects.filter(is_staff=False, is_superuser=False)

# Banners
@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AllBanner(SingleTableView):
	table_class = BannerTables
	model = Banner
	template_name = "list_view.html"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddBanner(SuccessMessageMixin, CreateView):
	model = Banner
	fields = "__all__"
	template_name = "form_view.html"
	success_message = "Banner Successfully Added"
	success_url = reverse_lazy("banners_list")

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateBanner(SuccessMessageMixin, UpdateView):
	model = Banner
	fields = "__all__"
	template_name = "form_view.html"
	success_message = "Banner Successfully Updated"
	success_url = reverse_lazy("banners_list")

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
