# Generated by Django 4.2 on 2023-08-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0025_alter_promoactivation_options_remove_customuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True),
        ),
    ]