from rest_framework import serializers
from menu_app.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'restaurant', 'day', 'day_display', 'open_time', 'close_time']

    def get_day_display(self, obj):
        return obj.get_day_display()
