# Generated by Django 4.2 on 2023-07-01 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_alter_cartitem_cart_favoritesitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='favoritesitem',
            unique_together={('user', 'product')},
        ),
    ]
