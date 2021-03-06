# Generated by Django 3.0.5 on 2021-05-21 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210521_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='show_in_homepage',
            field=models.BooleanField(default=False, verbose_name='نمایش در لندینگ'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.Brand', verbose_name='برند'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='قیمت'),
        ),
    ]
