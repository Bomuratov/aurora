from django.db import models
from django.contrib.auth.models import User
from django.db.models import SET_NULL, PROTECT, CASCADE
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
import io
from django.core.files.base import ContentFile

def thumbnail(image, size=(200, 200)):
    """
    Уменьшает изображение до указанного размера с сохранением пропорций.

    :param image: Загруженный объект файла (models.ImageField).
    :param size: Размер (ширина, высота) thumbnail'а.
    :return: Уменьшенный файл для сохранения в модели.
    """
    img = Image.open(image)
    img.thumbnail(size, Image.Resampling.LANCZOS)  # Уменьшает изображение

    # Сохранение в памяти
    img_io = io.BytesIO()
    img.save(img_io, format=img.format)
    return ContentFile(img_io.getvalue(), name=image.name)




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



class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(model_name)ss"
    )
    update_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(model_name)ss"
    )

    class Meta:
        abstract = True
        ordering = ("id",)



class Restaurant(BaseModel):
    user = models.ForeignKey("users.User", PROTECT, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    address = models.CharField(max_length=225)
    is_active = models.BooleanField(default=False)
    telegram_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    background_photo = models.FileField(upload_to=upload_path_rest, null=True, blank=False)
    logo = models.FileField(upload_to=upload_logo_rest, null=True, blank=False)
    editors = models.ManyToManyField("users.User", blank=True, related_name="editors") 
    availability_orders = models.BooleanField(default=False)
    orders_chat_id = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(-9999999999999), MaxValueValidator(9999999999999)]) 
    waiter_chat_id = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(-9999999999999), MaxValueValidator(9999999999999)])

    def __str__(self):
        return self.name


class Category(BaseModel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']


class Menu(BaseModel):
    name = models.CharField(max_length=225, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    photo = models.FileField(blank=True, upload_to=upload_path_menu, null=True)
    category = models.ForeignKey(
        Category, CASCADE, null=True, blank=True, related_name="title"
    )
    is_active = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    thumb = models.FileField(upload_to=upload_path_menu, null=True, blank=True)
    # slug = AutoSlugField(populate_from='name', null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.restaurant.name}"
    

    def save(self, *args, **kwargs):
        if self.photo:
            self.thumb = thumbnail(self.photo, size=(150, 150))
        return super().save(*args, **kwargs)




class Promo(BaseModel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.FileField(upload_to=upload_path_promo, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Promo is {self.restaurant.name}, {self.name}"