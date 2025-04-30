from rest_framework import viewsets, views, response, permissions
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema
from users.models import User
from users.serializers.user_serializer import UserSerializer



@extend_schema(tags=["User API"])
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
