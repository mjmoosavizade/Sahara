from products.models import Product
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from types import SimpleNamespace
from functools import lru_cache
from django.conf import settings
from os.path import join as join_path
from .models import Order, OrderProduct

def _city_fmt(json_data):
    province_table = {}
    for item in json_data:
        print (item["state"])
        if not (p:=item["province"]) in province_table.keys():
            province_table[p] = [item["state"]]
        else:
            if not item["state"] in province_table[p]:
                province_table[p].append(item["state"])
    return province_table

@lru_cache
def _load_json_file(file_path):
    path = join_path(settings.BASE_DIR, file_path)
    return json.load(open(path, "r", encoding="utf-8"))

@csrf_exempt
def cart(request): 
    if request.method == "POST":
        firstname = request.POST.get('firstname','')
        lastname = request.POST.get('lastname','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        province = request.POST.get('province','')
        city = request.POST.get('city','')
        items = request.POST.get('items','')
        item_obj = json.loads(json.loads(items))
        print(firstname)
        print(item_obj)
        print(type(item_obj))
        order = Order.objects.create(
            customer_fname=firstname,
            customer_lname=lastname,
            customer_phone=phone,
            customer_province=province,
            customer_city=city,
        )
        order.save()

        for item in item_obj:
            print (item)
            product = Product.objects.get(slug=item["slug"])
            OrderProduct.objects.create(product=product, order=order, quantity=item["qty"]).save()
        return HttpResponse("سفارش با موفقیت ثبت شد")
    else:
        print('checl')
        province_and_cities = _city_fmt(_load_json_file("cart/resources/citiesandstates.json"))
        return render(request, 'cart/cart.html', {
            "province_table": province_and_cities,
        })

