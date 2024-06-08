from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import SET_NULL, PROTECT, CASCADE
from django_extensions.db.fields import AutoSlugField




def upload_path_menu(instance, filename):
    file = filename.rfind(".")
    formatt = filename[file:]
    name = instance.name + formatt
    return "{0}/category/{1}/{2}".format(
        instance.restaurant.name, instance.category.name, name
    )


def upload_path_rest(instance, file):
    return "{0}/backgroud/{1}".format(instance.name, file)


def upload_logo_rest(instance, file):
    return "{0}/logo/{1}".format(instance.name, file)


def upload_path_promo(instance, filename):
    file = filename.rfind(".")
    formatt = filename[file:]
    name = instance.name + formatt
    return "{0}/promo/{1}/{2}".format(
        instance.restaurant.name, instance.name, name
    )




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
    is_active = models.BooleanField(default=False)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    instagramm = models.CharField(max_length=255, null=True, blank=True)
    photo = models.FileField(upload_to=upload_path_rest, null=True, blank=False)
    logo = models.FileField(upload_to=upload_logo_rest, null=True, blank=False)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(Basemodel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']


class Menu(Basemodel):
    name = models.CharField(max_length=225, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    photo = models.FileField(blank=True, upload_to=upload_path_menu, null=True)
    category = models.ForeignKey(
        Category, CASCADE, null=True, blank=True, related_name="title"
    )
    is_active = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.restaurant.name}"




class Promo(Basemodel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.FileField(upload_to=upload_path_promo, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Promo is {self.restaurant.name}, {self.name}"