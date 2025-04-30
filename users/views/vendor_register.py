from rest_framework import viewsets
from users.models import User
from drf_spectacular.utils import extend_schema
from users.serializers.vendor_register import VendorRegisterSerializer



@extend_schema(tags=["Authentication API"])
class VendorRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VendorRegisterSerializer
    lookup_field = "pk"