from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from types import SimpleNamespace

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
        print(items)
        item_obj = json.loads(items, object_hook=lambda d: SimpleNamespace(**d))
        print (item_obj)
    else:
        print('checl')
        return render(request, 'cart/cart.html')

