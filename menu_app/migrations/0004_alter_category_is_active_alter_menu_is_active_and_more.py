# Generated by Django 4.2.7 on 2025-04-27 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0003_menu_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='orders_chat_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='waiter_chat_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
