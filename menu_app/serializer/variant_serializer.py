from rest_framework import serializers
from menu_app.models import Variant, OptionGroup

class VariantCreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id",'name', 'price', 'is_active']


class VariantBulkCreateSerializer(serializers.Serializer):
    option_group = serializers.IntegerField()
    variants = VariantCreateItemSerializer(many=True)

    def create(self, validated_data):
        option_group_id = validated_data['option_group']
        option_group = OptionGroup.objects.get(id=option_group_id)
        variants_data = validated_data['variants']

        variants_to_create = [
            Variant(
                option_group=option_group,
                name=item["name"],
                price=item["price"],
                is_active=item.get("is_active", True)
            )
            for item in variants_data
        ]
        created_variants = Variant.objects.bulk_create(variants_to_create)
        return created_variants
