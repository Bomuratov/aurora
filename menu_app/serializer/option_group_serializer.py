from rest_framework import serializers
from menu_app.models import OptionGroup
from menu_app.serializer.variant_serializer import VariantCreateItemSerializer



class OptionGroupSerializer(serializers.ModelSerializer):
    variants = VariantCreateItemSerializer(many=True)

    class Meta:
        model = OptionGroup
        fields = ['id', 'variants']
        



