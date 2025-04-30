from rest_framework import serializers
from menu_app.models import Options


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = [
            "id",
            "menu",
            "size",
            "price",
        ]