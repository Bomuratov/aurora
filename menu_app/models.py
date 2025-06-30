from django.db import models
from django.db.models import SET_NULL, PROTECT, CASCADE
from django_extensions.db.fields import AutoSlugField
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
    return "{0}/promo/{1}/{2}".format(instance.restaurant.name, instance.name, name)


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(model_name)ss",
    )
    update_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_%(model_name)ss",
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
    background_photo = models.FileField(
        upload_to=upload_path_rest, null=True, blank=False
    )
    logo = models.FileField(upload_to=upload_logo_rest, null=True, blank=False)
    editors = models.ManyToManyField("users.User", blank=True, related_name="editors")
    availability_orders = models.BooleanField(default=False)
    orders_chat_id = models.BigIntegerField(null=True, blank=True)
    waiter_chat_id = models.BigIntegerField(null=True, blank=True)
    lat = models.CharField(max_length=225, null=True, blank=True)
    long = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_restaurant_editors(self):
        return self.editors


class Category(BaseModel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from="name", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


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
        return f"{self.name} in {self.restaurant}"

    def save(self, *args, **kwargs):
        if self.photo:
            self.thumb = thumbnail(self.photo, size=(150, 150))
        return super().save(*args, **kwargs)


class OptionGroup(BaseModel):
    menu = models.OneToOneField('menu_app.Menu', on_delete=models.CASCADE, related_name="options", null=True, blank=True)

    def __str__(self):
        return f"Options for {self.menu}"

class Variant(BaseModel):
    option_group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name="variants", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} – {self.price}"


class Promo(BaseModel):
    restaurant = models.ForeignKey(Restaurant, CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.FileField(upload_to=upload_path_promo, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Promo is {self.restaurant.name}, {self.name}"
    


class Schedule(BaseModel):

    class WeekDays(models.TextChoices):
        MONDAY = 0, "Понедельник"
        TUESDAY = 1, "Вторник"
        WEDNESDAY = 2, "Среда"
        THURSDAY = 3, "Четверг"
        FRIDAY = 4, "Пятница"
        SATURDAY = 5, "Суббота"
        SUNDAY = 6, "Воскресенье"

    restaurant = models.ForeignKey("menu_app.Restaurant", on_delete=models.CASCADE, null=True, blank=True, related_name="schedule")
    day = models.CharField(max_length=100, choices=WeekDays.choices)
    open_time = models.TimeField(db_index=True, null=True, blank=True)
    close_time = models.TimeField(db_index=True, null=True, blank=True)

    class Meta:
        # unique_together = ('restaurant', 'day')  # Один график на день
        ordering = ['day']

    def __str__(self):
        return f'{self.get_day_display()}: {self.open_time} - {self.close_time}'    


class DeliveryRule(BaseModel):
    CALCULATION_TYPE_CHOICES = [
        ('fixed', 'Фиксированная цена'),
        ('per_km', 'Цена за километр'),
        ('percent', 'Процент от суммы заказа'),

    ]

    restaurant = models.ForeignKey('menu_app.Restaurant', on_delete=models.CASCADE, related_name='delivery_rules')
    calculation_type = models.CharField(max_length=10, choices=CALCULATION_TYPE_CHOICES)
    min_distance = models.FloatField(null=True, blank=True)
    max_distance = models.FloatField(null=True, blank=True)
    fixed_price = models.PositiveIntegerField(null=True, blank=True)
    price_per_km = models.PositiveIntegerField(null=True, blank=True)
    price_per_percent = models.FloatField(null=True, blank=True)
    max_order_price_for_free_delivery = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.min_distance >= self.max_distance:
            raise ValidationError("Минимальное расстояние должно быть меньше максимального.")

        if self.calculation_type == 'fixed' and self.fixed_price is None:
            raise ValidationError("Укажите фиксированную цену.")
        if self.calculation_type == 'per_km' and self.price_per_km is None:
            raise ValidationError("Укажите цену за километр.")

    def __str__(self):
        title = f"{self.calculation_type.upper()} | {self.min_distance}-{self.max_distance} км"
        if self.calculation_type == 'fixed':
            title += f" | {self.fixed_price} сум"
        else:
            title += f" | {self.price_per_km} сум/км"
        return f"{self.restaurant.name} | {title}"


{
    "restaurant_id":3,
    "distance": 25,
    "order_price": 5650,
    "type":"percent"
}