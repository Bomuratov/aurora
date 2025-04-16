from rest_framework import serializers
from users.models import User
from users.serializers.user_location_serializer import UserLocationSerializer
from users.exceptions.validation_error import ValidateErrorException


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
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
            "location"
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
