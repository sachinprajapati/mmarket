from django.contrib import admin

from .models import *

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'img', 'parent')
#     search_fields = ('name', )

#     prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category)
admin.site.register(ProductClass)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Product)
admin.site.register(ProductImage)