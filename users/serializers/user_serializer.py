from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(), source="get_custom_permissions"
    )
    role=serializers.CharField(source="get_user_role")
    role_permissions = serializers.CharField(source="get_user_role_perms")

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
            "is_vendor",
            "role",
            "permissions",
            "role_permissions",
            ]