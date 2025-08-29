from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from menu_app.models import BaseModel, upload_logo_rest, upload_path_rest
from menu_app.util.phone_validators import UZB_PHONE_VALIDATOR
from menu_app.util.model_utils import thumbnail


class Restaurant(BaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, null=True, blank=True
    )
    name = models.CharField(max_length=225, null=True, blank=True)
    address = models.CharField(max_length=225)
    is_active = models.BooleanField(default=False)
    telegram_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    background_photo = models.FileField(
        upload_to=upload_path_rest, null=True, blank=False
    )
    native_background_photo = models.ImageField(
        upload_to=upload_path_rest, null=True, blank=True
    )
    native_thumb = models.ImageField(upload_to=upload_path_rest, null=True, blank=True)
    logo = models.FileField(upload_to=upload_logo_rest, null=True, blank=False)
    editors = models.ManyToManyField("users.User", blank=True, related_name="editors")
    availability_orders = models.BooleanField(default=False)
    orders_chat_id = models.BigIntegerField(null=True, blank=True)
    waiter_chat_id = models.BigIntegerField(null=True, blank=True)
    lat = models.CharField(max_length=225, null=True, blank=True)
    long = models.CharField(max_length=225, null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=255), blank=True, default=list)

    
    class Meta:
        indexes = [
            GinIndex(fields=["tags"]),  # создаём GIN-индекс для поиска по массиву
        ]
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.native_background_photo:
            self.native_thumb = thumbnail(self.native_background_photo, size=(600, 450))
        return super().save(*args, **kwargs)

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
    restaurant = models.ForeignKey(
        "menu_app.Restaurant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts",
    )
    phone_number = models.CharField(
        max_length=255, null=True, blank=True, validators=[UZB_PHONE_VALIDATOR]
    )

    def __str__(self):
        return f"Phone number of {self.restaurant.name} — {self.phone_number}"
