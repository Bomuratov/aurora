import json
import logging
from rest_framework import viewsets, response, permissions
from users.exceptions.validation_error import ValidateErrorException
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Menu, Category
from menu_app.serializers import MenuSerializer, PhotoMenuSerializer
from menu_app.utils import crop_image_by_percentage

logger = logging.getLogger(__name__)

@extend_schema(tags=["Menu API v1.01"])
class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name", "category_id"]
    
    def create(self, request):
        cat_id = request.data.get("category", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if cat_id:
            instance = bool(self.queryset.filter(category=int(cat_id), is_active=True))
            category = Category.objects.get(id=int(cat_id))
            category.is_active = instance
            category.save()

        return response.Response({"data": serializer.data})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        cat_id = request.data.get("category", None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if cat_id:
            instance = bool(self.queryset.filter(category=int(cat_id), is_active=True))
            category = Category.objects.get(id=int(cat_id))
            category.is_active = instance
            category.save()

        return response.Response(serializer.data)



            


@extend_schema(tags=["Menu Photo Update API v1.01"])
class UpdatePhotoMenu(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = PhotoMenuSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name", "category_id"]

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk == None:
            raise ValidateErrorException(detail="Не передан идентификатор продукта", code=2)
        try:
            instance = self.queryset.get(pk=pk)
        except:
            return response.Response(
                {
                    "message": "Не нашлось запись с переданным идентификатором",
                    "code": 1
                    
                }
            )
    
        resized_image = request.data.get("photo")
        sizes = request.data.get("crop")
        if resized_image:
            if sizes:
                sizes = json.loads(request.data["crop"])
                x = float(sizes["x"])
                y = float(sizes["y"])
                width = float(sizes["width"])
                height = float(sizes["height"])
                rotate = float(sizes["rotate"])
                scaleX = float(sizes["scaleX"])
                scaleY = float(sizes["scaleY"])
                request.data["photo"] = crop_image_by_percentage(
                    image_path=request.data["photo"],
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    scaleX=scaleX,
                    scaleY=scaleY,
                    rotate=rotate,
                )
        serializer = self.serializer_class(data=request.data, instance=instance, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
       
        return response.Response(serializer.data)
            