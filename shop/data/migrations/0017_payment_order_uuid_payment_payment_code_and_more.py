# Generated by Django 4.2 on 2023-06-10 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_order_shipping_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_uuid',
            field=models.CharField(default='ewfrefefe', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_code',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.paymentmethod'),
        ),
    ]