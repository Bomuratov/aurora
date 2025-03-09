from rest_framework import serializers
from menu_app.models import Promo, Restaurant



class PromoSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    photo = serializers.FileField(required=False)
    
    class Meta:
        model = Promo
        fields = "__all__"