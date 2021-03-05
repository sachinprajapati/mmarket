from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.db import connection
from products.models import Category, Product, ProductClass
from orders.models import Orders, ORDER_STATUS, OrderStatus

import django_tables2 as tables
from django_filters import rest_framework as filters, NumberFilter, ChoiceFilter, DateFilter, DateFromToRangeFilter
from django_filters.widgets import RangeWidget, DateRangeWidget
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Banner, AvailableAddress
from offer.models import Coupon

class ImageColumn(tables.Column):
    def render(self, value):
         return mark_safe('<img src="%s" width="60px;">' % escape(value.url))

class CategoryTable(tables.Table):
    img = ImageColumn(orderable=False, verbose_name="Image")
    get_update_url = tables.Column(verbose_name='Edit', orderable=False)
    class Meta:
        model = Category
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("name", "parent", "img", "get_update_url")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class ProductTable(tables.Table):
    get_update_url  = tables.Column(verbose_name='Edit', orderable=False)
    get_stock_url  = tables.Column(verbose_name='Stock', orderable=False)
    class Meta:
        model = Product
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("name", "price", "product_class", "categories", "get_update_url", "get_stock_url")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class ProductCLassTable(tables.Table):
    get_update_url  = tables.Column(verbose_name='Edit', orderable=False)
    class Meta:
        model = ProductClass
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("name", "require_shipping", "track_stock")

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class OrdersFilter(filters.FilterSet):
    amount__gt = NumberFilter(field_name='amount', lookup_expr='gt')
    amount__lt = NumberFilter(field_name='amount', lookup_expr='lt')
    status = ChoiceFilter(choices=ORDER_STATUS, method='status_filter')

    def status_filter(self, queryset, name, value):
        cursor = connection.cursor()
        cursor.execute('SELECT orders_orders.id as id FROM orders_orders left join orders_orderstatus on \
                            orders_orders.id=orders_orderstatus.order_id GROUP BY orders_orders.id HAVING \
                            MAX(orders_orderstatus.status)=%s;' % value)
        row = [i[0] for i in cursor.fetchall()]
        return queryset.filter(id__in=row)

    class Meta:
        model = Orders
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("order_id", "status", "customer__phone")

class OrdersTable(tables.Table):
    customer = tables.Column(orderable=False)
    product_count = tables.Column(verbose_name="No. Products", orderable=False)
    quantities = tables.Column(verbose_name="Total units", orderable=False)
    get_absolute_url = tables.Column(verbose_name="Detail", orderable=False)
    get_CurrentStatus = tables.Column(verbose_name="Status", orderable=False)
    class Meta:
        model = Orders
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("order_id", "amount", "get_CurrentStatus", "product_count", "quantities", "get_absolute_url")

    def render_get_absolute_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-info-circle"></span></a>' % escape(value))

    def render_customer(self, value):
        return mark_safe('<a href="%s"><span>%s</span></a>' % (escape(value.get_absolute_url()), escape(value.name)))

USER_STATUS = [
    (True, "Active"),
    (False, "Inactive")
]

class UsersFilter(filters.FilterSet):
    date_joined = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'placeholder': 'MM/DD/YYYY', 'type': 'date'}))
    is_active = ChoiceFilter(choices=USER_STATUS)
    # date_joined__lt = DateFilter(field_name='date_joined', lookup_expr='lt', label='Joined Before')
    class Meta:
        model = User
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("phone", "email", "is_active")

class UserList(tables.Table):
    get_absolute_url = tables.Column(orderable=False, verbose_name="Detail")
    email = tables.Column(orderable=False)
    phone = tables.Column(orderable=False)
    name = tables.Column(orderable=False)
    parent = tables.Column(verbose_name="Upline")
    class Meta:
        model = User
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("name", "phone", "email", "is_active", "parent", "date_joined", "get_absolute_url")

    def render_get_absolute_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-info-circle"></span></a>' % escape(value))

class BannerTables(tables.Table):
    get_update_url = tables.Column(verbose_name="Edit", orderable=False)
    img = tables.Column(orderable=False)
    get_delete_url = tables.Column(orderable=False, verbose_name='Delete')
    class Meta:
        model = Banner
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("img", "caption", "order", "get_update_url", "get_delete_url")

    def render_img(self, value):
         return mark_safe('<img src="%s" width="200px;">' % escape(value.url))

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

    def render_get_delete_url(self, value):
        return mark_safe('<a href="%s" onclick="YNconfirm(); return false;"><span class="fa fa-trash"></span></a>' % escape(value))

class AvailableAddressTable(tables.Table):
    get_update_url = tables.Column(verbose_name="Edit", orderable=False)
    class Meta:
        model = AvailableAddress
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ("pincode", )

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class CouponTables(tables.Table):
    total_discount = tables.Column(orderable=False)
    code = tables.Column(orderable=False)
    get_update_url = tables.Column(verbose_name="Edit", orderable=False)
    get_absolute_url = tables.Column(orderable=False, verbose_name="Detail")
    class Meta:
        model = Coupon
        attrs = {"class": "table table-hover table-bordered table-sm"}
        fields = ('name', 'code', 'discount_type', 'total_discount', 'date_created', 'get_absolute_url')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

    def render_get_absolute_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-info-circle"></span></a>' % escape(value))