from rest_framework import viewsets
from users.models import User
from users.serializers.vendor_register import VendorRegisterSerializer


class VendorRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VendorRegisterSerializer
    lookup_field = "pk"