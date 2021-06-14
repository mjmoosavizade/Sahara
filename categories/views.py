from products.views import product
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.text import slugify
from categories.models import Category
from products.models import Brand, Product

def categories(request):
    categories_list = Category.objects.all()
    if (selected_category:=request.GET.get("category", False)):
        products = Product.objects.filter(category__slug = selected_category)
    else:
        products = Product.objects.all()

    if (filter_on:=request.GET.get("filter")):
        filter_list = {
            "newest": products.order_by("-date_added"),
            "in-stock": products.filter(in_stock=True),
            "most-visited": products.order_by("-reviews_count")
        }
        if filter_on in filter_list.keys():
            products = filter_list[filter_on]
    brands = Brand.objects.filter(show_in_homepage = True)
    

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products =  paginator.get_page(page)

    context = {
        'categories' : categories_list,
        'products' : paged_products,
        'brands' : brands,
        'current_category' : selected_category,
        'filter_on': filter_on,
        "num_products": len(products)
    }

    return render(request, 'categories/categories.html', context)
