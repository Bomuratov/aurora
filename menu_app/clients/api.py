from menu_app.views import RestaurantView, CategoryView, MenuView, PromoView


class RestaurantClientView(RestaurantView):
    lookup_field="name"
    pass


class CategoryClientView(CategoryView):
    pass


class MenuClientView(MenuView):
    pass


class PromoClientView(PromoView):
    pass