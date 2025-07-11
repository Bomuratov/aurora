from rest_framework import viewsets
from users.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.serializers.vendor_register import VendorRegisterSerializer
from users.views.docs.register_docs import docs



@extend_schema_view(
    create=extend_schema(
        tags=docs.tags,
        description=docs.description.vendor_post
    )
)
class VendorRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VendorRegisterSerializer
    lookup_field = "pk"