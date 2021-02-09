from django import forms
from products.models import Product, Category, ProductImage, StockRecord
from orders.models import Orders

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column

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

class StockRecordForm(forms.ModelForm):
    num_in_stock = forms.IntegerField(disabled=True)
    add_quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('num_in_stock', css_class='form-group col-6 mb-0'),
                Column('add_quantity', css_class='form-group col-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

    class Meta:
        model = StockRecord
        fields = ("num_in_stock", )

    def save(self, commit=True):
        m = super(StockRecordForm, self).save(commit=False)
        if commit:
            m.num_in_stock += self.cleaned_data['add_quantity']
            m.save()
        return m