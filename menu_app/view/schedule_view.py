from rest_framework import viewsets
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.serializer.schedule_serializer import ScheduleSerializer
from menu_app.models import Schedule


class ScheduleView(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant_id"]
    lookup_field = "pk"

