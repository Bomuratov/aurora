from django.urls import include, path
from rest_framework.routers import SimpleRouter
from menu_app.admins.urls import urlpatterns as adminpatterns
from menu_app.clients.urls import urlpatterns as clientpatterns
from menu_app.admins.router import *
from menu_app.clients.router import *
from menu_app.utils import GenerateQR, DownloadQR

from menu_app.view import category_view, menu_view, promo_view, variant_view, schedule_view, delivery_rule_view, delivery_calculation

from menu_app.restaurant.views.web import restaurant_view
from menu_app.restaurant.views.native import restaurant_view_native


router = SimpleRouter()

router.register(r"restaurant", restaurant_view.RestaurantView, basename="restaurant")
router.register(r"native/restaurant", restaurant_view_native.RestaurantView, basename="restaurant")
router.register(r"category", category_view.CategoryView, basename="category")
router.register(r"menu", menu_view.MenuView, basename="menu")
router.register(r"promo", promo_view.PromoView, basename="promo")





urlpatterns = [
    path("api/admins/", include("menu_app.admins.urls")),
    path("api/client/", include("menu_app.clients.urls")),
    path('api/admins/categories/update_order/', CategoryView.as_view({'post': 'post_update'}), name='category_update_order'),
    path("api/admins/generate/qr", GenerateQR.as_view(), name='qr-generate'),
    path("api/admins/download/qr", DownloadQR.as_view(), name='qr-download'),

    path("api/v1/restaurant/<int:pk>", restaurant_view.RestaurantView.as_view({"get": "get_restaurant_by_id"}), name="get-restaurant-by-id"),

    # API FOT UPDATE AND GET PHOTO MENU
    path("api/v1/menu/thumb/<int:pk>", menu_view.UpdatePhotoMenu.as_view({"put": "update", "get": "retrieve"}), name='update-photo'),
    path("api/v1/menu/thumb/", menu_view.UpdatePhotoMenu.as_view({"get": "list"}), name='update-photo'),

    # API FOR GET FCM_TOKEN COURIERS
    path("api/v1/restaurant/channel/", restaurant_view.RestaurantChannelsView.as_view({"get": "list"}), name='restaurant-channel'),
    path("api/v1/restaurant/channel/<int:pk>", restaurant_view.RestaurantChannelsView.as_view({"get": "retrieve"}), name='restaurant-channel'),
    
    # API FOR GET EDITORS RESTAURANT
    path("api/v1/restaurant/editors/<int:pk>", restaurant_view.RestaurantEditorsView.as_view({"get": "retrieve"}), name='restaurant-editors'),

    # API FOR GET COURIERS RESTAURANT
    path("api/v1/restaurant/couriers/<int:pk>", restaurant_view.RestaurantCouriersView.as_view({"get": "retrieve"}), name='restaurant-editors'),
    path("api/v1/restaurant/courier/<int:pk>", restaurant_view.RestaurantCouriersView.as_view({"get": "get_restaurant_couriers"}), name='restaurant-editors'),
    
    # API FOR MENU VARIANTS
    path("api/v1/variant", variant_view.VariantView.as_view({"post": "create", "get": "list"}), name="menu-variant"),
    path("api/v1/variant/<int:pk>", variant_view.VariantView.as_view({"get": "retrieve", "delete":"destroy", "patch":"toggle_active"}), name="menu-variant-update"),

    # API FOR SCHEDULE RESTAURANT
    path("api/v1/restaurant/schedule", schedule_view.ScheduleView.as_view({"post":"create", "get":"list"}), name="restaurant-schedule"),
    path("api/v1/restaurant/schedule/<int:pk>", schedule_view.ScheduleView.as_view({"put":"update", "delete":"destroy", "get":"retrieve"}), name="restaurant-schedule"),
    path("api/v1/restaurant/<int:pk>/status", restaurant_view.RestaurantStatusView.as_view(), name="restaurant-status"),

    path("api/v1/category/menu/<int:pk>", menu_view.MenuFilterByCategoryView.as_view(), name="filter-menu-by-category"),

    path("api/v1/delivery/rule", delivery_rule_view.DeliveryRuleView.as_view({"get": "get_delivery_info"}), name="delivery-calculate"),
    path("api/v1/delivery/rules", delivery_rule_view.DeliveryRuleView.as_view({"get": "list", "post":"create"}), name="delivery-calculate"),
    path("api/v1/delivery/rules/<int:pk>", delivery_rule_view.DeliveryRuleView.as_view({"get": "retrieve", "put":"update", "delete":"destroy"}), name="delivery-calculate"),
    path("api/v1/delivery/rules/<int:pk>/active", delivery_rule_view.DeliveryRuleView.as_view({"post": "toggle_active"}), name="delivery-calculate"),

    path("api/v1/delivery/calculate", delivery_calculation.DeliveryCalculationView.as_view(), name="delivery-calculate"),

    # new routes
    path("api/v1/", include(router.urls)),
] 

# urlpatterns+=adminpatterns
# urlpatterns+=clientpatterns
