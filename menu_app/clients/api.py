from menu_app.views import RestaurantView, CategoryView, MenuView, PromoView
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["Restaurant API for clients"])
class RestaurantClientView(RestaurantView):
    lookup_field="name"
    pass

@extend_schema(tags=["Category API for clients"])
class CategoryClientView(CategoryView):
    pass

@extend_schema(tags=["Menu API for clients"])
class MenuClientView(MenuView):
    pass

@extend_schema(tags=["Promo API for clients"])
class PromoClientView(PromoView):
    pass