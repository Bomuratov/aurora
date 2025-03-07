from rest_framework import viewsets
from users.models import User
from users.serializers.register import UserRegisterSerializer


class UserRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = "pk"