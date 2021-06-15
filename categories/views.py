from itertools import chain
from products.views import product
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.text import slugify
from categories.models import Category
from products.models import Brand, Product

def _get_products_of_category(category):
    category_products = category.product_set.all()
    if len((children:=category.children.all())):
        for child in children:
            category_products |= _get_products_of_category(child)
    
    return category_products

def categories(request):
    categories_list = Category.objects.all()
    if (selected_category:=request.GET.get("category", False)) and selected_category != "False":
        #products = Product.objects.filter(category__slug = selected_category)
        products = _get_products_of_category(Category.objects.get(slug=selected_category))
    else:
        products = Product.objects.all()

    brand_name = ""
    if (brand_slug:=request.GET.get("brand", False)):
        brand = Brand.objects.get(slug=brand_slug)
        brand_name = brand.slug
        products = products.filter(brand=brand)

    if (filter_on:=request.GET.get("filter")):
        filter_list = {
            "newest": products.order_by("-date_added"),
            "in-stock": products.filter(in_stock=True),
            "most-visited": products.order_by("-reviews_count")
        }
        if filter_on in filter_list.keys():
            products = filter_list[filter_on]
    brands = Brand.objects.filter(show_in_homepage = True)
    

    paginator = Paginator(products, 20)
    page = request.GET.get('page', 1)
    paged_products =  paginator.get_page(page)

    context = {
        'categories' : categories_list,
        'products' : paged_products,
        'brands' : brands,
        'current_category' : selected_category,
        'filter_on': filter_on,
        "num_products": len(products),
        "page_number": page,
        "brand_name": brand_name
    }

    return render(request, 'categories/categories.html', context)
