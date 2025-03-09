from rest_framework import serializers
from menu_app.models import Menu



class MenuSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Menu
        fields = "__all__"