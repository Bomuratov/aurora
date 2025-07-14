from rest_framework import viewsets, decorators, response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.serializer.variant_serializer import VariantBulkCreateSerializer, VariantCreateItemSerializer
from menu_app.models import Variant, Menu, OptionGroup
from menu_app.view.docs.variant_docs import docs
from rest_framework.response import Response
from rest_framework import status


@extend_schema_view(
    list=extend_schema(tags=docs.tags, description=docs.description.get_list),
    retrieve=extend_schema(tags=docs.tags, description=docs.description.get_retrieve),
    create=extend_schema(tags=docs.tags, description=docs.description.create),
    update=extend_schema(tags=docs.tags, description=docs.description.update),
    destroy=extend_schema(tags=docs.tags, description=docs.description.destroy),
    toggle_active=extend_schema(tags=docs.tags, description=docs.description.update),
)
class VariantView(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantCreateItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("option_group__menu_id", "option_group_id")
    lookup_field= "pk"

    def create(self, request, *args, **kwargs):
        serializer = VariantBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_variants = serializer.save()
        response_serializer = VariantCreateItemSerializer(created_variants, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @decorators.action(detail=False, methods=["PATCH"])
    def toggle_active(self, request, pk):
        instance = self.get_object()
        if instance.is_active:
            instance.is_active = False
            instance.save()
            return response.Response({"message": "variant with ID: {} deacticvated".format(instance.id), "code": 2})
        elif not instance.is_active:
            instance.is_active = True
            instance.save()
            return response.Response({"message": "variant with ID: {} acticvated".format(instance.id), "code": 2})
        
        return response.Response({"message": "Не предвиденная ошибка отправьте запрос заново", "code": 5})



# from rest_framework.decorators import api_view
# from drf_spectacular.utils import extend_schema, OpenApiParameter
# from django.core.exceptions import PermissionDenied

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='rest', description='Ресторан ID', required=True, type=int),
#     ],
#     responses={200: "ok"}
# )
# @api_view(['GET'])
# def create_option_group(request):
#     user = request.user
#     id_rest = request.query_params.get("rest")
#     if user.is_superuser:
#         menu = Menu.objects.filter(restaurant_id=id_rest)
#         option_groups = [
#             OptionGroup(menu=menu_item, created_by=user) for menu_item in menu
#         ]
#         OptionGroup.objects.bulk_create(option_groups)
#         return Response({"detail": "ok"})
#     raise PermissionDenied()