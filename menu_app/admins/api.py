from menu_app.views import RestaurantView, CategoryView, MenuView
from rest_framework.permissions import IsAuthenticated





class RestaurantAdminView(RestaurantView):
    # permission_classes = (IsAuthenticated,)
    pass


class CategoryAdminView(CategoryView):
    # permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    pass


class MenuAdminView(MenuView):
    # permission_classes = (IsAuthenticated,)
    lookup_field="pk"
    pass
