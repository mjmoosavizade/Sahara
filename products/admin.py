from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'category', 'price')

admin.site.register(Product, ProductAdmin)

