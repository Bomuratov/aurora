from rest_framework import serializers
from users.models import UserSettings, User
from users.serializers.user_settings_serializer import UserSettingsSerializer
from users.serializers.user_serializer import UserSerializer
from menu_app.serializer.schedule_serializer import ScheduleSerializer
from datetime import datetime
from menu_app.restaurant.models import Restaurant






class RestaurantSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    schedule = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "created_by",
            "update_by",
            "user",
            "name",
            "address",
            "is_active",
            "telegram_link",
            "instagram_link",
            "background_photo",
            "logo",
            "native_background_photo",
            "native_thumb",
            "editors",
            "availability_orders",
            "orders_chat_id",
            "waiter_chat_id",
            "lat",
            "long",
            "schedule",
            "contacts",
            "is_open",
        ]

    def get_schedule(self, obj):
        if hasattr(obj, "schedule"):
            schedule = obj.schedule.all()
            return ScheduleSerializer(schedule, many=True).data
    
    def get_contacts(self, obj):
        if hasattr(obj, "contacts"):
            contacts = obj.contacts.all().values_list("phone_number", flat=True)
            return list(contacts)
        
    def get_is_open(self, obj):
        return obj.get_status()
    

    


class RestaurantChannels(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["id", "channels"]

    def get_channels(self, obj) -> dict:
        couriers = obj.editors.filter(role__role="is_courier")
        user_settings = UserSettings.objects.filter(user__in=couriers)
        return UserSettingsSerializer(user_settings, many=True).data


class RestaurantEditors(serializers.ModelSerializer):
    editors = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["id", "editors"]

    def get_editors(self, obj) -> dict:
        editors = obj.editors.all()
        return UserSerializer(editors, many=True).data


class RestaurantCouriersSerializer(serializers.ModelSerializer):
    couriers = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "couriers",
        ]

    def get_couriers(self, obj) -> dict:
        couriers = obj.editors.filter(role__role="is_courier")
        return UserSerializer(couriers, many=True).data
