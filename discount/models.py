from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(model_name)ss"
    )
    update_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(model_name)ss"
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("id",)


class PromoBackground(BaseModel):
    photo = models.ImageField(upload_to='promo/backgrounds', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class PromoCategory(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    ordering = models.PositiveBigIntegerField(default=0)
    background_photo = models.ForeignKey("discount.PromoBackground", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['ordering']


class Promo(BaseModel):
    restaurant = models.ForeignKey("menu_app.Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="", null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    

    def __str__(self) -> str:
        return f"Promo is {self.restaurant.name}, {self.name}"
    