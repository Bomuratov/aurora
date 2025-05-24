from rest_framework import serializers
from menu_app.models import Menu, Category, Options
from menu_app.serializer.options_serializer import OptionsSerializer



class MenuSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    options = OptionsSerializer(many=True, required=False, read_only=True)
    
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
            "options"
        )
    def create(self, validated_data):
        options = validated_data.pop('options', [])
        cat_id = validated_data["category"]
        data = Menu.objects.create(**validated_data)
        # for option in options:
        #     Options.objects.create(menu=data, **option)
        if cat_id:
            instance = bool(Menu.objects.filter(category=cat_id, is_active=True))  # тут возвращается либо Тру либо Фолс
            cat_id.is_active = instance # Берем инстанс Категории
            cat_id.save()

        return data
    

