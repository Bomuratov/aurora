from rest_framework import serializers
from menu_app.models import Menu, OptionGroup, Category
from menu_app.serializer.option_group_serializer import OptionGroupSerializer



class MenuSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    options = OptionGroupSerializer(required=False)
    category_label = serializers.SerializerMethodField()

    
    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "description",
            "price",
            "photo",
            "category",
            "category_label",
            "is_active",
            "availability",
            "restaurant",
            "thumb",
            "created_by",
            "update_by",
            "options"
        )
    def create(self, validated_data):
        cat_id = validated_data["category"]
        data = Menu.objects.create(**validated_data)
        OptionGroup.objects.create(menu=data)
        if cat_id:
            instance = bool(Menu.objects.filter(category=cat_id, is_active=True))  # тут возвращается либо Тру либо Фолс
            cat_id.is_active = instance # Берем инстанс Категории
            cat_id.save()

        return data
    
    def get_category_label(self, instance):
        return instance.category.name if instance.category else None

