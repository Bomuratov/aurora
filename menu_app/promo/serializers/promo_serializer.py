from rest_framework import serializers
from menu_app.promo.models.promo_model import Promo



class PromoSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Promo
        fields = "__all__"