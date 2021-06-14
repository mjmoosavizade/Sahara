from django.db import models
from django.utils.text import slugify 
from categories.models import Category
from datetime import datetime

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to = 'photos/brands/%Y/%m/%d/', blank = True, )
    show_in_homepage = models.BooleanField(default=False, verbose_name='نمایش در لندینگ')
    slug = models.SlugField(unique=True, editable=False)
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name, allow_unicode=True)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand_name

class ProductManager(models.Manager):
    def most_visited(self, n):
        """ returns `n` number of most visited products
        """
        return (self.order_by("-reviews_count")[:n] if n is not None
                else self.order_by("reviews_count"))

class Product(models.Model):
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    class Type(models.TextChoices):
        Stock = "Stock"
        Original = "Original"
    class Currency(models.TextChoices):
        Rial = "ًریال"
        Dollar = "$"
        Dirham = "درهم"

    objects = ProductManager()
    category = models.ForeignKey(Category, on_delete = models.DO_NOTHING, verbose_name='دسته بندی')
    product_name = models.CharField(max_length=255, verbose_name='نام محصول')
    description = models.TextField(verbose_name='توضیحات', null=False, blank=True)
    alternative_name_1 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_2 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_3 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_4 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, verbose_name='برند', blank=True)
    currency = models.CharField(max_length=8, choices=Currency.choices, default=Currency.Rial, verbose_name='ارز')
    price = models.IntegerField(null=True ,verbose_name='قیمت', blank=True, )
    slug = models.SlugField(unique=True, editable=False)
    product_photo = models.ImageField(upload_to= 'photos/product/%Y/%m/%d/', blank=True, verbose_name='تصویر محصول')
    type = models.CharField(max_length=8,choices= Type.choices, default=Type.Original, verbose_name='وضعیت')
    date_added = models.DateField(default=datetime.now, editable=False, blank=True)
    in_stock = models.BooleanField(default=True, verbose_name='موجودی')
    tech_spec = models.FileField(upload_to= 'spec/%Y/%m/%d/', blank=True, verbose_name='مشخصات محصول')
    show_in_homepage = models.BooleanField(default=False, verbose_name='نمایش در لندینگ')
    reviews_count = models.IntegerField(default=0, null=True, editable=False)

    @property
    def all_categories(self):
        categories = []
        current_category = self.category
        while current_category is not None:
            categories.append(current_category)
            current_category = current_category.parent
        return categories

    def increase_review(self):
        self.reviews_count+=1
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name