# Generated by Django 4.2 on 2023-06-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
