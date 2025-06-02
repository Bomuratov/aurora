from rest_framework import serializers
from menu_app.models import OptionGroup
from menu_app.serializer.variant_serializer import VariantSerializer



class OptionGroupSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = OptionGroup
        fields = ['id', 'variants']



