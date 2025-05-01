from rest_framework import serializers
from users.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ["user", "fcm_token", "device_type", "device_model"]