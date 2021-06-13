from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from categories.models import Category
from products.models import Brand, Product

def categories(request):
    categories_list = Category.objects.all()
    selected_category = ""
    # if 'category' in request.GET:
    #     selected_category = request.GET.get('category')
    #     products = Product.objects.filter(category__slug = selected_category)
    if (selected_category:=request.GET.get("category", False)):
        products = Product.objects.filter(category__slug = selected_category)
    else:
        products = Product.objects.all()
    brands = Brand.objects.filter(show_in_homepage = True)
    

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products =  paginator.get_page(page)

    context = {
        'categories' : categories_list,
        'products' : paged_products,
        'brands' : brands,
        'current_category' : selected_category,
    }

    return render(request, 'categories/categories.html', context)
