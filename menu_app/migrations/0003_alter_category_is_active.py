# Generated by Django 4.2.7 on 2025-04-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0002_rename_adress_restaurant_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
