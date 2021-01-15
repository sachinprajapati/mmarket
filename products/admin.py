from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'img', 'parent')
    search_fields = ('name', )

    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)