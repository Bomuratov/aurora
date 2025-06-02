from rest_framework import serializers
from menu_app.models import Restaurant
from users.models import UserSettings, User
from users.serializers.user_settings_serializer import UserSettingsSerializer
from users.serializers.user_serializer import UserSerializer



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
        
    def get_channels(self, obj) -> dict:
        couriers = obj.editors.filter(role__role="is_courier")
        user_settings = UserSettings.objects.filter(user__in=couriers)
        return UserSettingsSerializer(user_settings, many=True).data
    

class RestaurantEditors(serializers.ModelSerializer):
    editors = serializers.SerializerMethodField()
    class Meta:
        model = Restaurant
        fields = [
            "id",
            "editors"
            ]
        
    def get_editors(self, obj) -> dict:
        editors = obj.editors.all()
        return UserSerializer(editors, many=True).data