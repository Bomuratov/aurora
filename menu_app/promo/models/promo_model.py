from django.db import models
from shared.models import BaseModel
from shared.utils.image_paths import upload_path_promo


class Promo(BaseModel):
    restaurant = models.ForeignKey("menu_app.Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.FileField(upload_to=upload_path_promo, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Promo is {self.restaurant.name}, {self.name}"
    

class Discount(BaseModel):
    name = models.CharField(max_length=223, null=True, blank=True)
    