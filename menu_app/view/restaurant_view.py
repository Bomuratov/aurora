from rest_framework import viewsets, permissions, parsers
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Restaurant
from menu_app.serializer.restaurant_serializer import RestaurantSerializer



@extend_schema(tags=["Restaurant API v1.01"])
class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user_id', "name", "id")
    lookup_field = "name"