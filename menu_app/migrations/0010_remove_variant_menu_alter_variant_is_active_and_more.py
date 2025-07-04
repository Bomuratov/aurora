# Generated by Django 4.2.7 on 2025-06-02 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu_app', '0009_rename_size_variant_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='menu',
        ),
        migrations.AlterField(
            model_name='variant',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('menu', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='menu_app.menu')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='variant',
            name='option_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='menu_app.optiongroup'),
        ),
    ]
