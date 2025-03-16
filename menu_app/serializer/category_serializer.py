from rest_framework import serializers
from menu_app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Category
        fields = "__all__"

    def create(self, request, *args, **kwargs):
        print("Request data:", request)  # Выведет, что реально приходит
        return super().create(request, *args, **kwargs)