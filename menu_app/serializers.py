from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from menu_app.restaurant.models import Restaurant



class RestaurantSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Restaurant
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Category
        fields = [
            "id",
            "restaurant",
            "name",
            "order",
            "created_by",
            "update_by",
            "is_active",
        ]


class MenuSerializer(ModelSerializer):
    # restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # photo = serializers.FileField(required=False)

    class Meta:
        model = Menu
        fields = [
            "id",
            "name",
            "category",
            "restaurant",
            "price",
            "description",
            "photo",
            "is_active",
            "availability",
            "photo",
        ]
        extra_kwargs = {
            "category": {"required": True},
            "restaurant": {"required": True},
        }


class PromoSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    photo = serializers.FileField(required=False)

    class Meta:
        model = Promo
        fields = [
            "id",
            "restaurant",
            "name",
            "description",
            "price",
            "is_active",
            "photo",
            "created_by",
            "update_by",
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["vendor"] = ", ".join(
            Restaurant.objects.filter(user_id=user.id).values_list("name", flat=True)
        )
        return token


class PhotoMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ["id", "photo", "thumb"]



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
