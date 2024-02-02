from menu_app.views import RestaurantView, CategoryView, MenuView


class RestaurantClientView(RestaurantView):
    lookup_field="name"
    pass


class CategoryClientView(CategoryView):
    pass


class MenuClientView(MenuView):
    pass