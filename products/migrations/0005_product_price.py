# Generated by Django 3.0.5 on 2021-05-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True, verbose_name='قیمت'),
        ),
    ]
