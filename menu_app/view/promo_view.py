import json
from rest_framework import viewsets, response, permissions, status
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from menu_app.models import Promo
from menu_app.serializers import PromoSerializer
from menu_app.utils import crop_image_by_percentage


@extend_schema(tags=["Promo API v1.01"])
class PromoView(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name"]

    def create(self, request):
        if request.data["crop"]:
            sizes = json.loads(request.data["crop"])
            x = float(sizes["x"])
            y = float(sizes["y"])
            width = float(sizes["width"])
            height = float(sizes["height"])
            rotate = float(sizes["rotate"])
            scaleX = float(sizes["scaleX"])
            scaleY = float(sizes["scaleY"])
            request.data["photo"] = crop_image_by_percentage(
                image_path=request.data.get("photo", None),
                x=x,
                y=y,
                width=width,
                height=height,
                scaleX=scaleX,
                scaleY=scaleY,
                rotate=rotate,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"data": serializer.data})


    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return response.Response(
                {"message": "Предоставлен идентификатор заметки. Обновление невозможно", "code": 1},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            instance = self.queryset.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            return response.Response(
                {"message": "Запись не найден", "code": 2},
                status=status.HTTP_404_NOT_FOUND
            )
        resized_image = request.data.get("photo")
        sizes = request.data.get("crop")
        if resized_image and sizes:
            try:
                sizes = json.loads(sizes)
                x = float(sizes["x"])
                y = float(sizes["y"])
                width = float(sizes["width"])
                height = float(sizes["height"])
                rotate = float(sizes["rotate"])
                scaleX = float(sizes["scaleX"])
                scaleY = float(sizes["scaleY"])
                request.data["photo"] = crop_image_by_percentage(
                    image_path=resized_image,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    scaleX=scaleX,
                    scaleY=scaleY,
                    rotate=rotate,
                )
            except (KeyError, ValueError, TypeError) as e:
                return response.Response(
                    {"error": f"Invalid crop data: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = self.serializer_class(instance=instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"data": serializer.data}, status=status.HTTP_200_OK)