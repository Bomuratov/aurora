from rest_framework import serializers
from users.models import UserRole
from users.utils.constants import ROLES


class UserRoleSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ["id", "role", "label"]

    def get_label(self, instance):
        role_value = instance.role
        role_dict = dict(ROLES)
        return role_dict.get(role_value, None)
