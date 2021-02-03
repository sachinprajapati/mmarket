from django import forms
from products.models import Product, Category, ProductImage
from orders.models import Orders

class AddProduct(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent__isnull=False))
    field_order = ['name', 'upc', 'password', 'is_public', 'description', 'product_class', 'attributes', 'categories', 'mrp', 'price', 'is_discountable']
    class Meta:
        model = Product
        fields = "__all__"

class AddProductImage(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("img", "caption", "display_order", "product")

class OrderStatusForm(forms.ModelForm):
    order_id = forms.CharField(disabled=True)
    class Meta:
        model = Orders
        fields = ("order_id", "status")