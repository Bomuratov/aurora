import random
from datetime import timedelta
from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from users.models import User
from users.utils import unique_validator, phone_validator
from users.exceptions.validation_error import ValidateErrorException
from django.core.cache import cache


class UserRegisterSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "password_1",
            "password_2",
            "user_registered_at",
        ]
        read_only_fields = ["id", "user_registered_at"]

    def validate(self, attrs):
        if attrs["password_1"] != attrs["password_2"]:
            raise ValidateErrorException(detail="Пароли не совпадают", code=1)
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            is_active=True,
            is_user=True,
        )
        user.set_password(validated_data["password_1"])
        user.save()
        return user


class OtpCodeSerializer(serializers.Serializer):
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

    def create(self, validated_data):
        local_time = timezone.localtime(timezone.now())
        phone = validated_data["phone"]
        code = random.randint(100000, 999999)
        code_expiry = local_time + timedelta(minutes=30)
        max_code_try = 5
        code_max_out = local_time - timedelta(minutes=11)
        data = {
            "phone": phone,
            "code": code,
            "code_expiry": code_expiry,
            "max_code_try": max_code_try,
            "code_max_out": code_max_out,
        }
        key = f"otp:{phone}"
        cache.set(key, data)
        return data

"""
{
    "message": "OTP успешно генерирован.",
    "phone": "+998911234567",
    "code": 538725,
    "code_expiry": "2025-07-17T06:24:48.713722Z",
    "max_code_try": 0,
    "code_max_out": "2025-07-17T05:57:31.264694Z",
}
"""