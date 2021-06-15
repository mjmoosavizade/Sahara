from django.db import models
from products.models import Product


class Order(models.Model):
    customer_fname = models.CharField(
        max_length=255, verbose_name='نام مشتری', null=False)
    customer_lname = models.CharField(
        max_length=255, verbose_name='نام خانوادگی مشتری', null=False)
    customer_phone = models.CharField(
        max_length=255, verbose_name='شماره تماس', null=False)
    customer_province = models.CharField(max_length=255, verbose_name='استان')
    customer_city = models.CharField(max_length=255, verbose_name='شهر')
    is_delivered = models.BooleanField(default=False, null=True, verbose_name="تحویل داده شده؟")

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return f"{self.customer_fname} {self.customer_lname}, {self.customer_phone} [{'تحویل داده شده' if self.is_delivered else 'تحویل داده نشده'}]"


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity
