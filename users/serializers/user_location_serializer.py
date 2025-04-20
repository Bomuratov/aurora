from rest_framework import serializers
from users.models import UserLocation


class UserLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserLocation
        fields = "__all__"


    def create(self, validated_data):
        instance = UserLocation.objects.create(**validated_data)
        if instance.is_active:
            UserLocation.objects.filter(user=instance.user).exclude(pk=instance.pk).update(is_active=False)
        return instance
    
    
    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', instance.is_active)
        instance = super().update(instance, validated_data)
        if is_active:
            UserLocation.objects.filter(user=instance.user).exclude(pk=instance.pk).update(is_active=False)
        return instance
