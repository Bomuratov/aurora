from rest_framework import serializers
from menu_app.models import Menu, Category, Variant
from menu_app.serializer.variant_serializer import VariantSerializer



class MenuSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    variant = VariantSerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "description",
            "price",
            "photo",
            "category",
            "is_active",
            "availability",
            "restaurant",
            "thumb",
            "created_by",
            "update_by",
            "variant"
        )
    def create(self, validated_data):
        cat_id = validated_data["category"]
        data = Menu.objects.create(**validated_data)
        if cat_id:
            instance = bool(Menu.objects.filter(category=cat_id, is_active=True))  # тут возвращается либо Тру либо Фолс
            cat_id.is_active = instance # Берем инстанс Категории
            cat_id.save()

        return data
    

