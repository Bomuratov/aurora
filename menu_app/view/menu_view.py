import json
import logging
from rest_framework import viewsets, response, permissions, views, decorators
from users.exceptions.validation_error import ValidateErrorException
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.models import Menu, Category
from menu_app.serializer.menu_serializer import MenuSerializer
from menu_app.serializers import PhotoMenuSerializer
from menu_app.utils import crop_image_by_percentage
from menu_app.view.docs.menu_view_docs import docs
from django.db.models import Prefetch
from users.permissions.role_checks import RoleCheck
from menu_app.util.chunk import chunk_list


@extend_schema_view(
    list=extend_schema(tags=docs.tags, description=docs.description.get_list),
    retrieve=extend_schema(
        tags=["Menu API v1.01"], description="Получить один пункт меню по ID."
    ),
    create=extend_schema(
        tags=["Menu API v1.01"], description="Создать новый пункт меню."
    ),
    update=extend_schema(
        tags=["Menu API v1.01"], description="Полное обновление пункта меню (PUT)."
    ),
    partial_update=extend_schema(
        tags=["Menu API v1.01"], description="Частичное обновление пункта меню (PATCH)."
    ),
    destroy=extend_schema(
        tags=["Menu API v1.01"], description="Удаление пункта меню по ID."
    ),
)
class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [RoleCheck]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name", "category_id"]
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
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

    @decorators.action(methods=["GET"], detail=True)
    def chunk_menu(self, request, pk):
        categories = (
            Category.objects.filter(restaurant_id=int(pk))
            .order_by("order", "id")
            .prefetch_related(Prefetch("title", queryset=Menu.objects.order_by("id")))
        )

        out = []
        for i, cat in enumerate(categories):
            # header
            out.append(
                {
                    "type": "header",
                    "id": cat.id,
                    "title": (
                        "" if i == 0 else cat.name
                    ),
                }
            )
            # row
            products_qs = list(cat.title.all())
            products_serialized = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "description": p.description,
                    "photo": (
                        request.build_absolute_uri(p.photo.url) if p.photo else None
                    ),
                    "thumb": (
                        request.build_absolute_uri(p.thumb.url) if p.thumb else None
                    ),
                    "category": p.category_id,
                    "is_active": p.is_active,
                    "availability": p.availability,
                    "restaurant": p.restaurant_id,
                    "options": (
                        {
                            "id": p.option_group.id,
                            "variants": [
                                {
                                    "id": v.id,
                                    "name": v.name,
                                    "price": v.price,
                                    "is_active": v.is_active,
                                }
                                for v in p.option_group.variants.all()
                            ],
                        }
                        if p.option_group
                        else None
                    ),
                }
                for p in products_qs
            ]

            for idx, row in enumerate(chunk_list(products_serialized, 2)):
                out.append({"type": "row", "id": f"{cat.id}-{idx}", "products": row})

        return response.Response(out)



@extend_schema(tags=["Menu Photo Update API v1.01"])
class UpdatePhotoMenu(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = PhotoMenuSerializer
    permission_classes = [RoleCheck]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["restaurant__name", "category_id"]

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk == None:
            raise ValidateErrorException(
                detail="Не передан идентификатор продукта", code=2
            )
        try:
            instance = self.queryset.get(pk=pk)
        except:
            return response.Response(
                {"message": "Не нашлось запись с переданным идентификатором", "code": 1}
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
        serializer = self.serializer_class(
            data=request.data, instance=instance, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


class MenuFilterByCategoryView(views.APIView):
    def get(self, request, pk):
        # Готовим подзапрос для активных блюд
        active_menus_qs = Menu.objects.filter(is_active=True)

        # Загружаем категории с уже подгруженными активными блюдами
        categories = Category.objects.filter(
            restaurant_id=pk, is_active=True
        ).prefetch_related(
            Prefetch("title", queryset=active_menus_qs, to_attr="active_menus")
        )

        if not categories:
            return response.Response(
                {"message": "В данном заведении нет активных категорий."}
            )

        menu_of_categories = {}
        for category in categories:
            if category.active_menus:
                menu_of_categories[category.name] = MenuSerializer(
                    category.active_menus, many=True
                ).data

        if not menu_of_categories:
            return response.Response({"message": "Нет активных блюд в категориях."})

        return response.Response(menu_of_categories)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from menu_app.models import Menu, thumbnail


@api_view(["POST"])
def regenerate_thumbs(request, restaurant_id):
    """
    Пересоздает thumbnails для всех меню конкретного ресторана.
    """
    menus = Menu.objects.filter(restaurant_id=restaurant_id).exclude(photo__isnull=True)
    total = menus.count()

    if total == 0:
        return Response({"message": "Нет меню с фотографиями"}, status=status.HTTP_404_NOT_FOUND)

    updated = 0
    for menu in menus:
        try:
            if menu.photo:
                menu.thumb = thumbnail(menu.photo, size=(600, 450))  # всегда пересоздаем
                menu.save(update_fields=["thumb"])
                updated += 1
        except Exception as e:
            # Чтобы не падал весь цикл
            print(f"Ошибка у {menu.id}: {e}")

    return Response(
        {
            "message": f"Thumbnails пересозданы",
            "restaurant_id": restaurant_id,
            "total_menus": total,
            "updated": updated,
        },
        status=status.HTTP_200_OK,
    )


import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from menu_app.models import Menu


@api_view(["DELETE"])
def cleanup_unused_photos(request, restaurant_id):
    """
    Удаляет фото и thumbnails у ресторана, которые не привязаны к Menu.
    """
    menus = Menu.objects.filter(restaurant_id=restaurant_id)

    if not menus.exists():
        return Response(
            {"message": "Меню не найдено для ресторана", "restaurant_id": restaurant_id},
            status=status.HTTP_404_NOT_FOUND,
        )

    # собираем используемые пути
    used_files = set()
    for menu in menus:
        if menu.photo:
            used_files.add(menu.photo.path)
        if menu.thumb:
            used_files.add(menu.thumb.path)

    # путь к папке ресторана (если upload_path_menu кладёт туда)
    restaurant_name = menus.first().restaurant.name
    restaurant_dir = os.path.join(settings.MEDIA_ROOT, restaurant_name, "category")

    deleted = []

    if os.path.exists(restaurant_dir):
        for root, _, files in os.walk(restaurant_dir):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath not in used_files:
                    os.remove(filepath)
                    deleted.append(filepath)

    return Response(
        {
            "message": "Очистка завершена",
            "restaurant_id": restaurant_id,
            "deleted_count": len(deleted),
            "deleted_files": deleted,
        },
        status=status.HTTP_200_OK,
    )
