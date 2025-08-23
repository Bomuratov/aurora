from django.db import models
from django.db.models import PROTECT, CASCADE
from django_extensions.db.fields import AutoSlugField
from menu_app.util.model_utils import generate_description
from shared.models import BaseModel
from shared.utils.phone_validators import UZB_PHONE_VALIDATOR
from shared.utils.image_paths import thumbnail, upload_logo_rest, upload_path_menu, upload_path_promo, upload_path_rest


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
    

    def get_schedule_for_day(self, day: int):
        return self.schedule.filter(day=day)


    def get_today_schedule(self):
        from django.utils import timezone
        return self.get_schedule_for_day(timezone.localtime().weekday())


    def get_tomorrow_schedule(self):
        from django.utils import timezone
        tomorrow = (timezone.localtime().weekday() + 1) % 7
        return self.get_schedule_for_day(tomorrow)


    def get_status(self):
        from django.utils import timezone
        now = timezone.localtime()
        current_time = now.time()

        schedules_today = list(self.get_today_schedule())
        schedules_tomorrow = list(self.get_tomorrow_schedule())

        if not schedules_today:
            return False

        is_open = False

        for s in schedules_today:
            if s.open_time < s.close_time:
                if s.open_time <= current_time <= s.close_time:
                    is_open = True
                    break
            else:  # через полночь
                if current_time >= s.open_time or current_time <= s.close_time:
                    is_open = True
                    break

        if not is_open:
            for s in schedules_tomorrow:
                if s.open_time > s.close_time:
                    if current_time <= s.close_time:
                        is_open = True
                        break

        return is_open


class RestaurantDetails(BaseModel):
    restaurant = models.ForeignKey("menu_app.Restaurant", on_delete=models.CASCADE, null=True, blank=True, related_name="contacts")
    phone_number = models.CharField(max_length=255, null=True, blank=True, validators=[UZB_PHONE_VALIDATOR])

    def __str__(self):
        return f"Phone number of {self.restaurant.name} — {self.phone_number}"


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
            self.thumb = thumbnail(self.photo, size=(600, 450))
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
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_distance = models.FloatField(null=True, blank=True)
    max_distance = models.FloatField(null=True, blank=True)
    fixed_price = models.PositiveIntegerField(null=True, blank=True)
    price_per_km = models.PositiveIntegerField(null=True, blank=True)
    price_per_percent = models.FloatField(null=True, blank=True)
    max_order_price_for_free_delivery = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    reverse_calculate = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError
        if all([self.min_distance and self.max_distance]):
            if self.min_distance >= self.max_distance:
                raise ValidationError("Минимальное расстояние должно быть меньше максимального.")

        if self.calculation_type == 'fixed' and self.fixed_price is None:
            raise ValidationError("Укажите фиксированную цену.")
        if self.calculation_type == 'per_km' and self.price_per_km is None:
            raise ValidationError("Укажите цену за километр.")
        if self.calculation_type == 'percent' and self.price_per_percent is None:
            raise ValidationError("Укажите цену за километр.")
    
    
    def save(self, *args, **kwargs):
        self.clean()  # Вызов валидации

        generate_description(self)

        return super().save(*args, **kwargs)

            

    def __str__(self):
        title = f"{self.calculation_type.upper()} | {self.min_distance}-{self.max_distance} км"
        if self.calculation_type == 'fixed':
            title += f" | {self.fixed_price} сум"
        else:
            title += f" | {self.price_per_km} сум/км"
        return f"{self.restaurant.name} | {title}"


