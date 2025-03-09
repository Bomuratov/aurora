from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "avatar",
            "user_registered_at",
            "is_active",
            "is_user",
            "is_vendor"
            ]