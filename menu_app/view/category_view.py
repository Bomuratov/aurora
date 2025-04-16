from rest_framework import viewsets, decorators, response, status
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Category
from menu_app.serializer.category_serializer import CategorySerializer


@extend_schema(tags=["Category API v1.01"])
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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

    """
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNjkxMTU2LCJpYXQiOjE3NDE1MTgzNTYsImp0aSI6IjQ5ZDA5YmJjNmM4NjRiNTY5MmQ1M2ZjZDA4NGRlNWFiIiwidXNlcl9pZCI6MSwiZW1haWwiOiJhbnRpa2tvOTlAZ21haWwuY29tIiwiaXNfdXNlciI6dHJ1ZSwiaXNfdmVuZG9yIjp0cnVlLCJ2ZW5kb3IiOiJQYXN0YSBIb3VzZSwgc3RyaW5nMiJ9.V9I2vWM3ge1r6imY9Fysd-DZXFtprytGJHnWyQOLCGA
    """
