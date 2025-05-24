from rest_framework import serializers
from users.models import User
from users.serializers.user_location_serializer import UserLocationSerializer
from users.exceptions.validation_error import ValidateErrorException
from users.utils.constants import ROLES


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(), source="get_custom_permissions"
    )
    role=serializers.CharField(source="get_user_role")
    role_permissions = serializers.CharField(source="get_user_role_perms")
    role_label = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    channels = serializers.SerializerMethodField()
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
            "location",
            "permissions",
            "role",
            "role_label",
            "role_permissions",
            "channels",
            
            ]
        
    def get_location(self, instance):
        request = self.context.get("request", None)
        context = {"request": request}
        try:
            location = instance.user_location.filter(is_active=True).first()
            if location:
              return UserLocationSerializer(location, context=context).data
        except Exception as e:
            return ValidateErrorException(code=2, detail=e)
        return None
    
    def get_role_label(self, instance):
        role_value = instance.get_user_role()
        role_dict = dict(ROLES)
        return role_dict.get(role_value, None)
    
    def get_channels(self, instance):
        channels = instance.editors.values_list("id", flat=True)
        return channels
