from django.shortcuts import render
from categories.models import Category
from products.models import Brand, Product

def categories(request):
    categories_list = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.filter(show_in_homepage = True)

    context = {
        'categories' : categories_list,
        'products' : products,
        'brands' : brands,
    }

    return render(request, 'categories/categories.html', context)
