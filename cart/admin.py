from django.contrib import admin
from .models import Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct

class OrderAdmin(admin.ModelAdmin):
    ordering = ["-is_delivered"]
    inlines = [
        OrderProductInline
    ]

admin.site.register(Order, OrderAdmin)
