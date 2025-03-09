import json
from rest_framework import viewsets, response, status
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Menu, Category
from menu_app.serializer.menu_serializer import MenuSerializer
from menu_app.utils import crop_image_by_percentage


@extend_schema(tags=["Menu API v1.01"])
class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name"]
    
    def create(self, request, *args, **kwargs):
        crop_data = request.data.get("crop")
        if crop_data:
            try:
                sizes = json.loads(crop_data)
                x = float(sizes["x"])
                y = float(sizes["y"])
                width = float(sizes["width"])
                height = float(sizes["height"])
                rotate = float(sizes["rotate"])
                scaleX = float(sizes["scaleX"])
                scaleY = float(sizes["scaleY"])
                
                image_path = request.data.get("photo")
                if image_path:
                    request.data["photo"] = crop_image_by_percentage(
                        image_path=image_path,
                        x=x, y=y, width=width, height=height,
                        scaleX=scaleX, scaleY=scaleY, rotate=rotate
                    )
            except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
                return response.Response(
                    {"message": f"Данные для обработки фото неправилно: {str(e)}", "code": 2},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
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
        cat_id = request.data["category"]
        serializer.save()

        # Филтрация категории по активности
        instance = bool(self.queryset.filter(category=int(cat_id), is_active=True))

        # Филтрация категории для приминение изменение активности
        category = Category.objects.get(id=int(cat_id))
        category.is_active = instance
        category.save()
        return response.Response({"data": serializer.data})
