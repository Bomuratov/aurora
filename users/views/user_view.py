from rest_framework import viewsets, views, response, permissions
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema_view, extend_schema
from users.models import User
from users.serializers.user_serializer import UserSerializer
from users.views.docs.user_docs import docs

@extend_schema_view(
    list=extend_schema(
        tags=docs.tags,
        description=docs.description.get_list
    ),
    retrieve=extend_schema(
        tags=docs.tags,
        description=docs.description.get_retrieve
    ),
    update=extend_schema(
        tags=docs.tags,
        description=docs.description.update
    )
)
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
