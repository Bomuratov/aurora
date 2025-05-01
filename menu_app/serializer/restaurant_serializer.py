from rest_framework import serializers
from menu_app.models import Restaurant
from users.models import UserSettings
from users.serializers.user_settings_serializer import UserSettingsSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Restaurant
        fields = "__all__"

    
class RestaurantChannels(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "channels"
            ]
        
    def get_channels(self, obj):
        couriers = obj.editors.filter(role__role="is_courier")
        user_settings = UserSettings.objects.filter(user__in=couriers)
        return UserSettingsSerializer(user_settings, many=True).data