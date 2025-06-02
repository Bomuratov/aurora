from rest_framework import serializers
from menu_app.models import Variant


class VariantListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        variants = [Variant(**item) for item in validated_data]
        return Variant.objects.bulk_create(variants)


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            "menu",
            "name",
            "price",
        ]
        list_serializer_class = VariantListSerializer