from django import forms
from products.models import Product, Category, ProductImage

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

ProductImageFormset = forms.modelformset_factory(ProductImage, exclude=("product", ), max_num=6, min_num=1, form=AddProductImage,can_delete=True)