from django.shortcuts import render
from categories.models import Category
from products.models import Product, Brand
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import translation


def index(request):
    print (translation.get_language())
    categories = Category.objects.filter(show_in_homepage=True)
    products = Product.objects.filter(show_in_homepage=True)
    sample_products = Product.objects.most_visited(10)
    brands = Brand.objects.filter(show_in_homepage=True)
    context = {
        'categories': categories,
        'products': products,
        'sample_products': sample_products,
        'brands': brands
    }

    return render(request, 'pages/index.html', context)


def search(request):
    queryset_product = Product.objects.all()
    keyword = request.GET.get('keyword', False)
    if keyword:
        queryset_product = queryset_product.filter(
            Q(product_name__icontains=keyword)       |
            Q(alternative_name_1__icontains=keyword) |
            Q(alternative_name_2__icontains=keyword) |
            Q(alternative_name_3__icontains=keyword) |
            Q(alternative_name_4__icontains=keyword) |
            Q(brand__brand_name__icontains=keyword)  |
            Q(category__category_title__icontains=keyword))
    products = []
    for i in queryset_product:
        temp_obj = {}
        temp_obj['id'] = i.id
        temp_obj['slug'] = i.slug
        temp_obj['product_name'] = i.product_name
        temp_obj['category'] = i.category.category_title
        if(i.description):
            temp_obj['description'] = i.description
        else:
            temp_obj['description'] = ""

        if(i.alternative_name_1):
            temp_obj['alternative_name_1'] = i.alternative_name_1
        else:
            temp_obj['alternative_name_1'] = "..."
        if(i.alternative_name_2):
            temp_obj['alternative_name_2'] = i.alternative_name_2
        else:
            temp_obj['alternative_name_2'] = "..."
        if(i.alternative_name_3):
            temp_obj['alternative_name_3'] = i.alternative_name_3
        else:
            temp_obj['alternative_name_3'] = "..."
        if(i.alternative_name_4):
            temp_obj['alternative_name_4'] = i.alternative_name_4
        else:
            temp_obj['alternative_name_4'] = "..."
        temp_obj['brand'] = i.brand.brand_name
        temp_obj['currency'] = i.currency
        if(i.price):
            temp_obj['price'] = i.price
        else:
            temp_obj['price'] = "تماس بگیرید"
        if(i.product_photo):
            temp_obj['product_photo'] = i.product_photo.url
        else:
            temp_obj['product_photo'] = ""

        temp_obj['type'] = i.type
        temp_obj['in_stock'] = i.in_stock
        if(i.tech_spec):
            temp_obj['tech_spec'] = i.tech_spec.url
        else:
            temp_obj['tech_spec'] = ""
        products.append(temp_obj)
    paginated_products = Paginator(products, request.GET.get("items_per_page", 15))
    page_number = int(request.GET.get("page", 1)) # returns page 1 by default
    paged_products = paginated_products.get_page(page_number)
    
    return JsonResponse({
        'results': paged_products.object_list,
        'num_pages': paginated_products.num_pages,
        'page_number': page_number,
        'num_products': len(products), 
    })


def get_product(request):

    keyword = request.GET.get('slug')
    product = Product.objects.filter(slug=keyword)[0]

    temp_obj = {}
    temp_obj['slug'] = product.slug
    temp_obj['product_name'] = product.product_name
    temp_obj['category'] = product.category.category_title
    if(product.description):
        temp_obj['description'] = product.description
    else:
        temp_obj['description'] = "..."
    if(product.alternative_name_1):
        temp_obj['alternative_name_1'] = product.alternative_name_1
    else:
        temp_obj['alternative_name_1'] = "..."
    if(product.alternative_name_2):
        temp_obj['alternative_name_2'] = product.alternative_name_2
    else:
        temp_obj['alternative_name_2'] = "..."
    if(product.alternative_name_3):
        temp_obj['alternative_name_3'] = product.alternative_name_3
    else:
        temp_obj['alternative_name_3'] = "..."
    if(product.alternative_name_4):
        temp_obj['alternative_name_4'] = product.alternative_name_4
    else:
        temp_obj['alternative_name_4'] = "..."
    temp_obj['brand'] = product.brand.brand_name
    temp_obj['currency'] = product.currency
    if(product.price):
        temp_obj['price'] = product.price
    else:
        temp_obj['price'] = "تماس بگیرید"
    if(product.product_photo):
        temp_obj['product_photo'] = product.product_photo.url
    else:
        temp_obj['product_photo'] = ""
    temp_obj['type'] = product.type
    temp_obj['in_stock'] = product.in_stock
    if(product.tech_spec):
        temp_obj['tech_spec'] = product.tech_spec.url
    else:
        temp_obj['tech_spec'] = ""

    return JsonResponse({'results': temp_obj})
