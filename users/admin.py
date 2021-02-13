from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(WalletHistory)