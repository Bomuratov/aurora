from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(model_name)ss"
    )
    update_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(model_name)ss"
    )

    class Meta:
        abstract = True
        ordering = ("id",)
