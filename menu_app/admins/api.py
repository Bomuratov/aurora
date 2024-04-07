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
        return Response({"image": serializer.data})


class PromoAdminView(PromoView):
    # permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    pass
