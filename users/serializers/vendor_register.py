from rest_framework import serializers
from django.conf import settings
from users.utils import phone_validator, unique_validator
from menu_app.restaurant.models import Restaurant
from users.models import User, UserSettings
from users.exceptions.validation_error import ValidateErrorException


class VendorRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[
            phone_validator.UZB_PHONE_VALIDATOR,
            unique_validator.UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с такими данными уже существует.",
                code="2",
            ),
        ]
    )
    password_1 = serializers.CharField(
        required=True,
        write_only=True,
        min_length=settings.PASSWORD_MIN_LENGTH,
        error_messages={
            "min_length": f"Парол должен быть больше {settings.PASSWORD_MIN_LENGTH} символов"
        },
    )
    password_2 = serializers.CharField(
        required=True,
        write_only=True,
        min_length=settings.PASSWORD_MIN_LENGTH,
        error_messages={
            "min_length": f"Парол должен быть больше {settings.PASSWORD_MIN_LENGTH} символов"
        },
    )
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), write_only=True
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password_1",
            "password_2",
            "role",
            "permissions",
            "restaurant_id", 
        ]

    def validate(self, attrs):
        if attrs["password_1"] != attrs["password_2"]:
            raise ValidateErrorException(detail="Пароли не совпадают", code=1)
        return attrs

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        restaurant = validated_data.pop("restaurant_id", None)
        user = User.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            phone = validated_data["phone"],
            role = validated_data["role"],
            is_vendor = True,
            is_active = True,
            is_user = True,
        )
        
        if restaurant:
            restaurant.editors.add(user)

        user.permissions.set(permissions)
        user.set_password(validated_data["password_1"])
        user.save()
        user_settings = UserSettings.objects.create(user=user)
        user_settings.save()
        return user