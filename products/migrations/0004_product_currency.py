# Generated by Django 3.0.5 on 2021-05-21 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210517_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[('ًریال', 'Rial'), ('$', 'Dollar'), ('درهم', 'Dirham')], default='ًریال', max_length=8, verbose_name='ًقیمت'),
        ),
    ]
