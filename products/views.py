from django.shortcuts import render

def product(request, product_id):
    return render(request, 'products/product.html')