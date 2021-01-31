import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape
from products.models import Category, Product, ProductClass
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