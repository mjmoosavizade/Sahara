from django.db import models
from django.utils.text import slugify 
from django.core.validators import MinValueValidator 
from categories.models import Category

class Product(models.Model):
    class Type(models.TextChoices):
        Stock = "Stock"
        Original = "Original"
    class Currency(models.TextChoices):
        Rial = "ًریال"
        Dollar = "$"
        Dirham = "درهم"

    category = models.ForeignKey(Category, on_delete = models.DO_NOTHING, verbose_name='دسته بندی')
    product_name = models.CharField(max_length=255, verbose_name='نام محصول')
    alternative_name_1 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_2 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_3 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    alternative_name_4 = models.CharField(max_length=255, blank=True, verbose_name='نام های دیگر')
    currency = models.CharField(max_length=8, choices=Currency.choices, default=Currency.Rial, verbose_name='ارز')
    price = models.IntegerField(null=True ,verbose_name='قیمت', validators=[MinValueValidator(1)])
    slug = models.SlugField(unique=True, editable=False)
    product_photo = models.ImageField(upload_to= 'photos/product/%Y/%m/%d/', blank=True, verbose_name='تصویر محصول')
    type = models.CharField(max_length=8,choices= Type.choices, default=Type.Original, verbose_name='وضعیت')
    tech_spec = models.FileField(upload_to= 'spec/%Y/%m/%d/', blank=True, verbose_name='مشخصات محصول')
    show_in_homepage = models.BooleanField(default=False, verbose_name='نمایش در لندینگ')

    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name