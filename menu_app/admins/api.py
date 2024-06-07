from rest_framework.permissions import IsAuthenticated
from rest_framework import status, response
from menu_app.views import RestaurantView, CategoryView, MenuView, PromoView
from menu_app.utils import image_resize, image_resize_asyc, crop_image_by_percentage
from menu_app.models import Category
import json




class RestaurantAdminView(RestaurantView):
    # permission_classes = (IsAuthenticated,)
    pass


class CategoryAdminView(CategoryView):
    permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    pass


class MenuAdminView(MenuView):
    permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    
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
            cropped_img = crop_image_by_percentage(
                image_path=request.data.get("photo", None),
                x=x,
                y=y,
                width=width,
                height=height,
                scaleX=scaleX,
                scaleY=scaleY,
                rotate=rotate,
            )
            request.data["photo"] = cropped_img
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"data": serializer.data})

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return response.Response(
                {
                    "Ошибочка": "Вы не передали идентификатор записи метод UPDATE не определeн"
                }
            )
        try:
            instance = self.queryset.get(pk=pk)
        except:
            return response.Response(
                {"Ошибочка": "Не нашлось запись с переданным идентификатором"}
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
        serializer = self.serializer_class(data=request.data, instance=instance)
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



class PromoAdminView(PromoView):
    permission_classes = (IsAuthenticated,)
    lookup_field="pk"

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
                {"error": "ID not provided. UPDATE method not defined."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            instance = self.queryset.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            return response.Response(
                {"error": "Record with the provided ID not found."},
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