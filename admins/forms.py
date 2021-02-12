from django import forms
from django.utils.translation import gettext_lazy as _
from products.models import Product, Category, ProductImage, StockRecord
from orders.models import Orders, OrderStatus
from offer.models import Coupon

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
        model = OrderStatus
        fields = ("status",)

class StockRecordForm(forms.ModelForm):
    num_in_stock = forms.IntegerField(disabled=True)
    num_allocated = forms.IntegerField(disabled=True)
    add_quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('num_in_stock', css_class='form-group col-4 mb-0'),
                Column('num_allocated', css_class='form-group col-4 mb-0'),
                Column('add_quantity', css_class='form-group col-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

    class Meta:
        model = StockRecord
        fields = ("num_in_stock", "num_allocated")

    def save(self, commit=True):
        m = super(StockRecordForm, self).save(commit=False)
        if commit:
            m.num_in_stock += self.cleaned_data['add_quantity']
            m.save()
        return m

class CouponForm(forms.ModelForm):
    on_category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent__isnull=False), help_text=_("Select category to avail. "
                             "Leave this empty to select all category."), blank=True, required=False)
    # on_category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent__isnull=False), widget=forms.CheckboxSelectMultiple)
    start_datetime = forms.DateField(required=False, widget = forms.TextInput(attrs={'type': 'date'}))
    end_datetime = forms.DateField(required=False, widget = forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('discount_type', css_class='form-group col-md-3 mb-0'),
                Column('total_discount', css_class='form-group col-md-3 mb-0'),
                Column('min_order', css_class='form-group col-md-3 mb-0'),
                Column('applicable_on', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('max_user_applications', css_class='form-group col-md-3 mb-0'),
                Column('start_datetime', css_class='form-group col-md-3 mb-0'),
                Column('end_datetime', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('offer_type', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('on_category', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
    class Meta:
        model = Coupon
        fields = "__all__"