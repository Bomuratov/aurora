from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.models import Restaurant
from menu_app.serializer.restaurant_serializer import RestaurantSerializer, RestaurantChannels, RestaurantEditors
from menu_app.view.docs.restaurant_view_docs import docs



@extend_schema_view(
    list=extend_schema(
        tags=docs.tags,
        description=docs.description.get_list
    ),
    retrieve=extend_schema(
        tags=docs.tags,
        description=docs.description.get_retrieve
    ),
    create=extend_schema(
        tags=docs.tags,
        description=docs.description.create
    ),
    update=extend_schema(
        tags=docs.tags,
        description=docs.description.update
    ),
    partial_update=extend_schema(
        tags=docs.tags,
        description=docs.description.partial_update
    ),
    destroy=extend_schema(
        tags=docs.tags,
        description=docs.description.destroy
    ),
    
)
class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user_id', "name", "id")
    lookup_field = "name"
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    list=extend_schema(
        tags=docs.tags,
        description=docs.description.get_channel_pm
    ),
    retrieve=extend_schema(
        tags=docs.tags,
        description=docs.description.get_channel
    ),
)
class RestaurantChannelsView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantChannels
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user_id', 'id')
    lookup_field = "pk"


@extend_schema_view(
    retrieve=extend_schema(
        tags=docs.tags,
        description=docs.description.get_editors
    ),
)
class RestaurantEditorsView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantEditors
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', "name")
    lookup_field = "pk"