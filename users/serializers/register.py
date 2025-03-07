# from rest_framework import serializers
# from django.conf import settings
# from users.models import User
# from users.utils import unique_validator, phone_validator
# from users.exceptions.validation_error import ValidateErrorException


# class UserRegisterSerializer(serializers.ModelSerializer):
#     phone = serializers.CharField(
#         validators=[
#             phone_validator.UZB_PHONE_VALIDATOR,
#             unique_validator.UniqueValidator(
#                 queryset=User.objects.all(),
#                 message="Пользователь с такими данными уже существует.",
#                 code="2",
#             ),
#         ]
#     )
#     email = serializers.EmailField(
#         validators=[
#             unique_validator.UniqueValidator(
#                 queryset=User.objects.all(),
#                 message="Пользователь с такими данными уже существует.",
#                 code="2",
#             )
#         ]
#     )
#     password_1 = serializers.CharField(
#         required=True,
#         write_only=True,
#         min_length=settings.PASSWORD_MIN_LENGTH,
#         error_messages={
#             "min_length": f"Парол должен быть больше {settings.PASSWORD_MIN_LENGTH} символов"
#         },
#     )
#     password_2 = serializers.CharField(
#         required=True,
#         write_only=True,
#         min_length=settings.PASSWORD_MIN_LENGTH,
#         error_messages={
#             "min_length": f"Парол должен быть больше {settings.PASSWORD_MIN_LENGTH} символов"
#         },
#     )

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "first_name",
#             "last_name",
#             "phone",
#             "email",
#             "password_1",
#             "password_2",
#             "user_registered_at",
#         ]
#         read_only_fields = ["id", "user_registered_at"]

#     def validate(self, attrs):
#         if attrs["password_1"] != attrs["password_2"]:
#             raise ValidateErrorException(detail="Пароли не совпадают", code=1)
#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             first_name=validated_data["first_name"],
#             last_name=validated_data["last_name"],
#             phone=validated_data["phone"],
#             email=validated_data["email"],
#             is_active = True,
#             is_user = True,
#         )
#         user.set_password(validated_data["password_1"])
#         user.save()
#         return  user
        
