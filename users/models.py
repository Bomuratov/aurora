from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from users.utils.phone_validator import INTERNATIONAL_PHONE_VALIDATOR
from users.utils.constants import PERMISSIONS, ROLES
from django.contrib.contenttypes.models import ContentType


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
    phone=models.CharField(max_length=14, null=True, blank=True, unique=True, validators=[INTERNATIONAL_PHONE_VALIDATOR])
    avatar = models.ImageField(upload_to="media", null=True)
    telegram_id = models.PositiveBigIntegerField(null=True, blank=True)
    user_registered_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey("users.UserRole", on_delete=models.SET_NULL, null=True, blank=True, related_name="user_role")
    permissions = models.ManyToManyField("users.Permissions", related_name="user_perms", blank=True)

    USERNAME_FIELD = "phone"
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} – {self.phone}"
    
    def has_custom_perm(self, perm, obj=None):
        return perm in self.get_custom_permissions() if perm else None

    def get_custom_permissions(self):
        return list(self.permissions.values_list("perms", flat=True)) if self.permissions else None
    
    def get_user_role(self):
        return self.role.role if self.role else None
    
    def get_user_role_perms(self):
        return self.role.permissions if self.role else None 


class Permissions(models.Model):
    code = models.CharField(choices=PERMISSIONS, max_length=255)
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    perms = models.CharField(null=True, blank=True, max_length=225)

    def __str__(self):
        return f"{self.code}_{self.content.model}"
    
    def save(self, *args, **kwargs):
        if self.content:
            self.perms = f"{self.code}_{self.content.model}"
        super().save(*args, **kwargs)
    
    class Meta:
        default_permissions = ()
    

class UserRole(models.Model):
    role = models.CharField(choices=ROLES, max_length=255)
    code = models.ManyToManyField(Permissions, related_name="roles")
    permissions = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.role

class UserLocation(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, related_name="user_location")
    lat = models.CharField(max_length=255, null=True, blank=True)
    long = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=225, null=True, blank=True)
    apartment = models.CharField(max_length=225, null=True, blank=True)
    floor = models.CharField(max_length=225, null=True, blank=True)
    entrance = models.CharField(max_length=225, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return f"location of {self.user}"
    
    class Meta:
        ordering = ['id']