from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'phone', 'is_active', 'is_staff', 'parent')

admin.site.register(User, UserAdmin)
admin.site.register(Wallet)
admin.site.register(WalletHistory)