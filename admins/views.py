from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import F
from django.db.models.aggregates import Max
from django.forms import modelformset_factory

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView

from django.contrib.auth import get_user_model
User = get_user_model()

from products.models import *
from orders.models import *
from offer.models import Coupon
from .tables import *
from users.models import Maintance
from basket.models import CartLine
from .forms import *
from datetime import date

# Create your views here.
@staff_member_required(login_url=reverse_lazy('login'))
def index(request):
	# user = User.objects.filter(is_staff=False, is_superuser=False)
	# user = User.objects.raw("select * from %s" %User._meta.db_table)
	# print('user is', user.columns)
	user = User.objects.filter(is_staff=False, is_superuser=False)
	order = Orders.objects.filter()
	product = Product.objects.filter()
	cw = CartLine.objects.filter()
	context = {
		"users": {
			"total" : len(user),
			"active": len([i for i in user if i.is_active==True]),
			"new": len([i for i in user if i.date_joined.date()>=date.today()])
		},
		"orders": {
			"total": order.count(),
			"pending": len(OrderStatus.StatusWith(0)),
			"delivered": len(OrderStatus.StatusWith(4))
		},
		"products":{
			"total": product.count(),
			"out": 10
		},
		"cw": {
			"total": len(cw)
		}
	}
	print(context)
	return render(request, 'index.html', context)

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
class AllProducts(SingleTableMixin, FilterView):
	queryset = Product.objects.filter()
	template_name = 'list_view.html'
	table_class = ProductTable
	filterset_class = ProductFilter

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddProducts(SuccessMessageMixin, CreateView):
	form_class = AddProduct
	template_name = "form_view1.html"
	success_url = reverse_lazy('products_list')
	success_message = "%(name)s successfully created"

	def get_success_url(self):
		return reverse_lazy('add_product_images', args=(self.object.id,))

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateProducts(SuccessMessageMixin, UpdateView):
	form_class = AddProduct
	template_name = "form_view1.html"
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
	queryset = Category.objects.filter()
	template_name = 'list_view.html'
	table_class = CategoryTable

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateCategory(SuccessMessageMixin, UpdateView):
	template_name = "form_view.html"
	model = Category
	# fields = "__all__"
	form_class = CategoryForm
	success_message = "%(name)s successfully updated"
	success_url = reverse_lazy('categories-list')

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddCategories(SuccessMessageMixin, CreateView):
	# model = Category
	# fields = ('name', 'parent', 'img')
	form_class = CategoryForm
	template_name = "form_view.html"
	success_url = reverse_lazy('categories-list')
	success_message = "%(name)s successfully created"

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
			if hasattr(product, 'stockrecord'):
				return redirect(reverse_lazy('product_attribute', kwargs={'pk': product.pk}))
			return redirect(reverse_lazy('product_attribute', kwargs={'pk': product.pk}))
	return render(request, template_name, {
		'formset': formset,
		'product': product,
	})

@staff_member_required(login_url=reverse_lazy('login'))
def AddProductsAttribute(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if hasattr(product.product_class, 'productattribute_set'):
		att = ProductAttributeValue.objects.filter(attribute__in=product.product_class.productattribute_set.all(), product=product)
	else:
		att = None
	print("att is",att)
	if not att:
		if hasattr(product, 'stockrecord'):
			return HttpResponseRedirect(reverse_lazy('update_stock', kwargs={'pk': product.pk}))
		return HttpResponseRedirect(reverse_lazy('product_stock', kwargs={'pk': product.pk}))
	if request.method == "POST":
		data = request.POST
		for i,j in data.items():
			if i != 'csrfmiddlewaretoken':
				attr = att.get(attribute__id=i)
				field_type = 'value_'+attr.attribute.type
				epv = ProductAttributeValue.objects.filter(attribute=attr.attribute, product=product)
				if epv.exists():
					epv.update(**{field_type: j})
				else:
					dc = {'attribute_id': attr.pk, 'product_id': product.pk, field_type: j}
					pv = ProductAttributeValue(**dc)
					print("pv is", pv)
					pv.save()

		messages.success(request, 'Product attribute successfully added')
		if hasattr(product, 'stockrecord'):
			return HttpResponseRedirect(reverse_lazy('update_stock', kwargs={'pk': product.pk}))
		return HttpResponseRedirect(reverse_lazy('product_stock', kwargs={'pk': product.pk}))
	context = {
		'att': att,
		'product': product
	}
	if request.method == "POST":
		pass
	return render(request, 'attribute_form.html', context)

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddProductStock(SuccessMessageMixin, CreateView):
	model = StockRecord
	fields = ('num_in_stock', 'low_stock_threshold')
	success_message = "product stock record created"
	template_name = "form_view.html"
	success_url = reverse_lazy("products_list")

	def form_valid(self, form):
		form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
		return super(AddProductStock, self).form_valid(form)

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateProductStock(SuccessMessageMixin, UpdateView):
	form_class = StockRecordForm
	template_name = "form_view1.html"
	success_message = "product stock record updated"
	success_url = reverse_lazy("products_list")

	def get_object(self, queryset=None):
		return get_object_or_404(StockRecord, pk=self.kwargs['pk'])


@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateOrders(SuccessMessageMixin, CreateView):
	template_name = "form_view1.html"
	form_class = OrderStatusForm
	success_message = "Status successfully updated"
	success_url = reverse_lazy('orders_list')

	def get_initial(self):
		initial = super().get_initial()
		initial['order_id'] = self.get_object().order_id
		initial['order'] = self.get_object().pk
		initial['expected_datetime'] = self.get_object().expected_dt if self.get_object().expected_dt else None
		initial['status'] = self.get_object().get_Status()
		return initial

	def get_object(self):
		return get_object_or_404(Orders, pk=self.kwargs.get('pk'))

	# def form_valid(self, form):
	# 	form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
	# 	return super(UpdateOrders, self).form_valid(form)

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

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DeleteBanner(DeleteView):
	model = Banner
	success_url = reverse_lazy('banners_list')
	template_name = 'banner_confirm_delete.html'

# Pincode

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class PincodeList(SingleTableView):
	table_class = AvailableAddressTable
	model = AvailableAddress
	template_name = "list_view.html"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddPincode(SuccessMessageMixin, CreateView):
	model = AvailableAddress
	fields = "__all__"
	template_name = "form_view.html"
	success_message = "Pincode Successfully Added"
	success_url = reverse_lazy("pincode_list")

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdatePincode(SuccessMessageMixin, UpdateView):
	model = AvailableAddress
	fields = "__all__"
	template_name = "form_view.html"
	success_message = "Pincode Successfully Updated"
	success_url = reverse_lazy("pincode_list")

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddCouponView(SuccessMessageMixin, CreateView):
	model = Coupon
	form_class = CouponForm
	template_name = "form_view1.html"
	success_url = reverse_lazy('coupon_list')
	success_message = _("Coupon successfully created")

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class ListCouponView(SingleTableView):
	model = Coupon
	template_name = "list_view.html"
	table_class = CouponTables
	queryset = Coupon.objects.all()

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateCouponView(SuccessMessageMixin, UpdateView):
	model = Coupon
	template_name = "form_view1.html"
	form_class = CouponForm
	success_url = reverse_lazy('coupon_list')
	success_message = _("Coupon successfully updated")

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DetailCouponView(DetailView):
	model = Coupon
	template_name = "form_view1.html"

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateDebug(SuccessMessageMixin, UpdateView):
	model = Maintance
	success_url = reverse_lazy('dashboard')
	success_message = "Application Status Successfully updated"
	template_name = "form_view.html"
	fields = ("status","message")

	def get_object(self, queryset=None):
		if self.model.objects.filter(status__in=[True, False]).exists():
			return self.model.objects.filter()[0]
		else:
			obj = self.model.objects.create()
			obj.save()
			return obj

@staff_member_required(login_url=reverse_lazy('login'))
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('dashboard'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'form_view.html', {
        'form': form
    })

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class CreateDiscount(SuccessMessageMixin, CreateView):
	model = ProductDiscount
	form_class = ProductDiscountForm
	template_name = 'form_view.html'
	success_message = 'Discount on product successfully created'
	success_url = reverse_lazy('list_discount')

	def get_initial(self):
		data = super(CreateDiscount, self).get_initial()
		data['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
		return data

	def form_valid(self, form):
		form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
		return super(CreateDiscount, self).form_valid(form)

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class UpdateDiscount(SuccessMessageMixin, UpdateView):
	model = ProductDiscount
	form_class = ProductDiscountForm
	template_name = 'form_view.html'
	success_message = 'Discount on product successfully updated'
	success_url = reverse_lazy('list_discount')

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class ListDiscount(SingleTableMixin, FilterView):
	model = ProductDiscount
	template_name = 'list_view.html'
	table_class = ProductDiscountTable
	filterset_class = ProductDiscountFilter