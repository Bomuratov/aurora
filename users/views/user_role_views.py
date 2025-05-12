from django.http import JsonResponse
from rest_framework import viewsets, response
from users.models import UserRole
from users.serializers.user_role_serializer import UserRoleSerializer
from users.utils.constants import ROLES
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["USER ROLE API'S"])
class UserRoleView(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    lookup_field = "pk"


@extend_schema(tags=["USER ROLE LABEL API'S"])
def get_role_labels(request):
    role_choices = [
        {"value": role[0], "label": role[1]} for role in ROLES
    ]
    return JsonResponse({"role": role_choices})