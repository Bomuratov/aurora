import json
from rest_framework import viewsets, response, permissions
from users.exceptions.validation_error import ValidateErrorException
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Menu, Category
from menu_app.serializers import MenuSerializer, PhotoMenuSerializer
from menu_app.utils import crop_image_by_percentage


@extend_schema(tags=["Menu API v1.01"])
class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name", "category_id"]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"data": serializer.data})



            


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
        # cat_id = request.data["category"]

        # Филтрация категории по активности
        # instance = bool(self.queryset.filter(category=int(cat_id), is_active=True))

        # # Филтрация категории для приминение изменение активности
        # category = Category.objects.get(id=int(cat_id))
        # category.is_active = instance
        # category.save()
        return response.Response(serializer.data)
            