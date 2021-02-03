from django.utils.safestring import mark_safe
from django.utils.html import escape
from products.models import Category, Product, ProductClass
from orders.models import Orders

import django_tables2 as tables
from django_filters import rest_framework as filters, NumberFilter, ChoiceFilter
from django.contrib.auth import get_user_model
User = get_user_model()
import itertools

class ImageColumn(tables.Column):
    def render(self, value):
         return mark_safe('<img src="%s" width="60px;">' % escape(value.url))

class CategoryTable(tables.Table):
    img = ImageColumn(orderable=False, verbose_name="Image")
    get_update_url = tables.Column(verbose_name='Edit', orderable=False)
    class Meta:
        model = Category
        template_name = "django_table2/bootstrap.html"
        fields = ("name", "parent", "img", "get_update_url")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class ProductTable(tables.Table):
    get_update_url  = tables.Column(verbose_name='Edit', orderable=False)
    class Meta:
        model = Product
        template_name = "django_table2/bootstrap.html"
        fields = ("name", "price", "product_class", "categories", "get_update_url")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class ProductCLassTable(tables.Table):
    get_update_url  = tables.Column(verbose_name='Edit', orderable=False)
    class Meta:
        model = ProductClass
        template_name = "django_table2/bootstrap.html"
        fields = ("name", "price", "product_class", "categories", "get_update_url")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class OrdersFilter(filters.FilterSet):
    amount__gt = NumberFilter(field_name='amount', lookup_expr='gt')
    amount__lt = NumberFilter(field_name='amount', lookup_expr='lt')
    class Meta:
        model = Orders
        fields = ("order_id", "status")

class OrdersTable(tables.Table):
    customer = tables.Column(orderable=False)
    product_count = tables.Column(verbose_name="No. Products", orderable=False)
    quantities = tables.Column(verbose_name="Total units", orderable=False)
    get_absolute_url = tables.Column(verbose_name="Detail", orderable=False)
    class Meta:
        model = Orders
        template_name = "django_table2/bootstrap.html"
        fields = ("order_id", "amount", "status", "product_count", "quantities", "get_absolute_url")

    def render_get_absolute_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-info-circle"></span></a>' % escape(value))

    def render_customer(self, value):
        return mark_safe('<a href="%s"><span>%s</span></a>' % (escape(value.get_absolute_url()), escape(value.name)))

USER_STATUS = [
    ('', "All"),
    (True, "Active"),
    (False, "Inactive")
]

class UsersFilter(filters.FilterSet):
    is_active = ChoiceFilter(choices=USER_STATUS)
    class Meta:
        model = User
        fields = ("phone", "email", "is_active")

class UserList(tables.Table):
    get_absolute_url = tables.Column(orderable=False, verbose_name="Detail")
    email = tables.Column(orderable=False)
    phone = tables.Column(orderable=False)
    name = tables.Column(orderable=False)
    class Meta:
        model = User
        template_name = "django_table2/bootstrap.html"
        fields = ("name", "phone", "email", "is_active", "date_joined", "get_absolute_url")

    def render_get_absolute_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-info-circle"></span></a>' % escape(value))