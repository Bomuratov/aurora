# Generated by Django 4.2.7 on 2025-05-01 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_merge_20250430_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(choices=[('is_supervisor', 'Супервайзер'), ('is_manager', 'Менеджер'), ('is_director', 'Директор'), ('is_analytic', 'Аналитик'), ('is_hr', 'HR'), ('is_agent', 'Агент'), ('is_courier', 'Курьер'), ('is_dispatcher', 'Диспетчер'), ('is_operator', 'Оператор')], max_length=255),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcm_token', models.TextField(db_index=True)),
                ('device_type', models.CharField(blank=True, max_length=250, null=True)),
                ('device_model', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
