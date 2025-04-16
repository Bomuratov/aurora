from rest_framework import viewsets
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


    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id is None:
            raise ValidateErrorException(detail="Такой API эндпоить не сушествует", code=2)
        return UserLocation.objects.filter(user_id=user_id)
        
