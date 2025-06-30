from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.models import User
from users.serializers.register import UserRegisterSerializer
from users.views.docs.register_docs import docs



@extend_schema_view(
    create=extend_schema(
        tags=docs.tags,
        description=docs.description.user_post
    )
)


@extend_schema(tags=["Authentication API"])
class UserRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = "pk"