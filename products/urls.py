from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.product, name='product')
]
