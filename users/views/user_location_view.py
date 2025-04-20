from rest_framework import viewsets, response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from users.serializers.user_location_serializer import UserLocationSerializer
from users.models import UserLocation
from users.exceptions.validation_error import ValidateErrorException


@extend_schema(tags=["User Location API"])
class UserLocationView(viewsets.ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["user_id"]
    lookup_field = "pk"      

    @action(detail=True, methods=["PATCH"])
    def toggle_active(self, request, pk=None):
        instance = self.get_object()
        if not instance.is_active:
            instance.is_active=True
            instance.save()
            UserLocation.objects.filter(user=instance.user).exclude(pk=instance.pk).update(is_active=False)
            return response.Response({"message": "is_active успешно изменен", "code": 2})
        return response.Response({"message": "is_active и так True", "code": 3})
