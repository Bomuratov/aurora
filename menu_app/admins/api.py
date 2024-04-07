from menu_app.views import RestaurantView, CategoryView, MenuView, PromoView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from menu_app.utils import image_resize





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
        request.data["photo"] = image_resize(request.data["photo"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})
    
    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Ошибочка": "Вы не передали идентификатор записи метод UPDATE не определeн"})
        try:
            instance = self.queryset.get(pk=pk)
        except:
            return Response({"Ошибочка": "Не нашлось запись с переданным идентификатором"})
        if request.data["photo"]:
            request.data["photo"] = image_resize(request.data["photo"])
        serializer = self.serializer_class(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})


class PromoAdminView(PromoView):
    # permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    pass
