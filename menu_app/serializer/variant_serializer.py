from rest_framework import serializers
from menu_app.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            "menu",
            "name",
            "price",
        ]