from django.shortcuts import render
from categories.models import Category
from products.models import Product
from django.http import JsonResponse
from django.core.serializers import serialize


def index(request):
    categories = Category.objects.filter(show_in_homepage=True)
    products = Product.objects.filter(show_in_homepage=True)
    sample_products = Product.objects.all()[:10]
    context = {
        'categories': categories,
        'products': products,
        'sample_products': sample_products,
    }

    return render(request, 'pages/index.html', context)


def search(request):
    queryset_product = Product.objects.all()
    keyword = request.GET.get('keyword')
    if 'keyword' in request.GET.get('keyword'):
        queryset_product = queryset_product.filter(
            product_name__icontains=keyword,
            alternative_name_1__icontains=keyword,
            alternative_name_2__icontains=keyword,
            alternative_name_3__icontains=keyword,
            alternative_name_4__icontains=keyword,
            brand__icontains=keyword,
            category__icontains=keyword)

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

    return JsonResponse({'results': products})


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
