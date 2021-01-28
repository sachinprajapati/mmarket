from django.contrib import admin

from .models import *

admin.site.register(Address)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(OrderPayment)
