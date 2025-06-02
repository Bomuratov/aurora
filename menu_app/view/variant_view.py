from rest_framework import viewsets
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.serializer.variant_serializer import VariantSerializer
from menu_app.models import Variant
from menu_app.view.docs.variant_docs import docs


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
    destroy=extend_schema(
        tags=docs.tags,
        description=docs.description.destroy
    )
)

class VariantView(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('menu_id',)
    lookup_field = "id"