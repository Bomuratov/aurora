from rest_framework import serializers
from menu_app.models import DeliveryRule


class DeliveryRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryRule
        fields = [
            "id",
            "restaurant",
            "name",
            "description",
            "calculation_type",
            "min_distance",
            "max_distance",
            "price_per_km",
            "fixed_price",
            "price_per_percent",
            "max_order_price_for_free_delivery",
            "is_active",
        ]
