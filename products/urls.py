from django.urls import re_path
from . import views

urlpatterns = [
    re_path('(?P<slug>[\w-]+)/$', views.product, name='product')
]
