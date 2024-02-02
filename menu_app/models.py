from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import SET_NULL, PROTECT, CASCADE
from .utils import upload_path_rest, upload_logo_rest, upload_path_menu
from django_extensions.db.fields import AutoSlugField


class Basemodel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    created_by = models.ForeignKey(
        User, SET_NULL, null=True, blank=True, related_name="created_%(model_name)ss"
    )
    update_by = models.ForeignKey(
        User, SET_NULL, null=True, blank=True, related_name="updated_%(model_name)ss"
    )

    class Meta:
        abstract = True
        ordering = ("id",)


class Restaurant(Basemodel):
    user = models.ForeignKey(User, PROTECT, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    adress = models.CharField(max_length=225)
    photo = models.FileField(upload_to=upload_path_rest, null=True, blank=False)
    logo = models.FileField(upload_to=upload_logo_rest, null=True, blank=False)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(Basemodel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return self.name


class Menu(Basemodel):
    name = models.CharField(max_length=225, null=True, blank=False)
    description = models.CharField(max_length=225, null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    photo = models.FileField(blank=True, upload_to=upload_path_menu, null=True)
    category = models.ForeignKey(
        Category, CASCADE, null=True, blank=True, related_name="title"
    )
    is_active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.restaurant.name}"


