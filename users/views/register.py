from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from users.models import User
from users.serializers.register import UserRegisterSerializer


@extend_schema(tags=["Authentication API"])
class UserRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = "pk"