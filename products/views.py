from django.shortcuts import render
from .models import Product

def product(request, slug):
    product = Product.objects.filter(slug = slug).first()
    product.increase_review()

    context = {
        'product':product
    }

    return render(request, 'products/product.html', context)