from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from users.utils.phone_validator import UZB_PHONE_VALIDATOR


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("User must have a username")
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone=phone, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_user = True
        user.is_vendor = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone=models.CharField(max_length=14, null=True, blank=True, unique=True, validators=[UZB_PHONE_VALIDATOR])
    avatar = models.ImageField(upload_to="media", null=True)
    telegram_id = models.PositiveBigIntegerField(null=True, blank=True)
    user_registered_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} – {self.phone}"


class UserLocation(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, related_name="user_location")
    lat = models.CharField(max_length=255, null=True, blank=True)
    long = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=225, null=True, blank=True)
    apartment = models.CharField(max_length=225, null=True, blank=True)
    floor = models.CharField(max_length=225, null=True, blank=True)
    entrance = models.CharField(max_length=225, null=True, blank=True)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return f"location of {self.user}"