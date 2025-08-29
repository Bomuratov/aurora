from rest_framework import serializers
from menu_app.restaurant.models.restaurant import RestaurantDetails



class RestaurantDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantDetails
        fields = ["phone_number"]