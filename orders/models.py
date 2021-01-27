from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from django.conf import settings

from products.models import Product

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{10}',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone = models.DecimalField(validators=[phone_regex], max_digits=10, decimal_places=0)
    pin_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{6}', message="Pincode number must be 6 digits long.")
    pincode = models.PositiveIntegerField(validators=[pin_regex])
    house = models.CharField(max_length=255, verbose_name=_("Flat, House no., Building"))
    area = models.CharField(max_length=255, verbose_name=_("Area, Street, Village"))
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=40)
    desc = models.TextField(verbose_name=_("Address Description"), blank=True, null=True)

ORDER_STATUS = [
    (1, 'Pending'),
    (2, 'Processing'),
    (3, 'Rejected'),
    (4, 'Completed'),
]

class Orders(models.Model):
    id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ORDER_STATUS, default=1, verbose_name=_("Order Status"))
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveSmallIntegerField()

