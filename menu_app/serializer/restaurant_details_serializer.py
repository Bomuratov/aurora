from rest_framework import serializers
from menu_app.models import RestaurantDetails


class RestaurantDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantDetails
        fields = ["phone_number"]