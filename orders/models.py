from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product

ADDRESS_TYE = [
    (1, 'Home'),
    (2, 'Office')
]

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
    type = models.PositiveSmallIntegerField(choices=ADDRESS_TYE)
    desc = models.TextField(verbose_name=_("Address Description"), blank=True, null=True)

ORDER_STATUS = [
    (1, 'Pending'),
    (2, 'Processing'),
    (3, 'Rejected'),
    (4, 'Completed'),
]

def Order_ID():
    now = timezone.localtime()
    return now.strftime('%Y%m%d%H%M%S%f')

class Orders(models.Model):
    order_id = models.CharField(max_length=20, unique=True, default=Order_ID)
    amount = models.IntegerField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ORDER_STATUS, default=1, verbose_name=_("Order Status"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    expected_dt = models.DateField(null=True, verbose_name="Expected Delivery Date")
    dt = models.DateTimeField(auto_now_add=True)

    @property
    def get_payment_type(self):
        return self.orderpayment.type

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveSmallIntegerField()

@receiver(post_save, sender=Orders)
def place_order(sender, instance, created, **kwargs):
    if created:
        cart_item = instance.customer.cart.lines.all()
        l = []
        for i in cart_item:
            l.append(OrderItems(order=instance, product=i.product, quantity=i.quantity, price=i.price))
        OrderItems.objects.bulk_create(l)
        cart_item.delete()

PAYMENT_TYPE = [
    (1, 'COD'),
    (2, 'Online'),
]

class OrderPayment(models.Model):
    order = models.OneToOneField(Orders, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    type = models.PositiveIntegerField(choices=PAYMENT_TYPE)
    tid = models.CharField(max_length=255, null=True)
    dt = models.DateTimeField(auto_now_add=True)



