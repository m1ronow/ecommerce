# Generated by Django 4.2 on 2023-06-07 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_product_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='currency',
        ),
    ]
