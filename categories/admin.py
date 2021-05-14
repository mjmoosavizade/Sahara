from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_title', 'parent')

admin.site.register(Category, CategoryAdmin)