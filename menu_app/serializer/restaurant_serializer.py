from rest_framework import serializers
from menu_app.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Restaurant
        fields = "__all__"