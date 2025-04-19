from rest_framework import serializers
from users.models import UserLocation


class UserLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserLocation
        fields = "__all__"


