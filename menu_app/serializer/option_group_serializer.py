from rest_framework import serializers
from menu_app.models import OptionGroup, Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'price']


class OptionGroupSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = OptionGroup
        fields = ['id', 'variants']



