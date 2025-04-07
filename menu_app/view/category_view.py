from rest_framework import viewsets, decorators, response, status
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Category
from menu_app.serializer.category_serializer import CategorySerializer
from users.permissions.role_checks import RoleCheck, PermissionCheck


@extend_schema(tags=["Category API v1.01"])
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[RoleCheck]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name"]

    @decorators.action(detail=False, methods=["post"], url_path="update_order")
    @extend_schema(tags=["Category API v1.01"])
    def post_update(self, request):
        category_ids = request.data
        for index, category_id in enumerate(category_ids):
            category = Category.objects.get(id=category_id)
            category.order = index
            category.save()
        return response.Response({"message": "ok"}, status=status.HTTP_200_OK)

  
