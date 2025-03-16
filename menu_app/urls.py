from django.urls import include, path
from rest_framework.routers import SimpleRouter
from menu_app.admins.urls import urlpatterns as adminpatterns
from menu_app.clients.urls import urlpatterns as clientpatterns
from menu_app.admins.router import *
from menu_app.clients.router import *
from menu_app.utils import GenerateQR, DownloadQR

from menu_app.view import restaurant_view, category_view, menu_view, promo_view



router = SimpleRouter()

router.register(r"restaurant", restaurant_view.RestaurantView, basename="restaurant")
router.register(r"category", category_view.CategoryView, basename="category")
router.register(r"menu", menu_view.MenuView, basename="menu")
router.register(r"promo", promo_view.PromoView, basename="promo")




urlpatterns = [
    path("api/admins/", include("menu_app.admins.urls")),
    path("api/client/", include("menu_app.clients.urls")),
    path('api/admins/categories/update_order/', CategoryView.as_view({'post': 'post_update'}), name='category_update_order'),
    path("api/admins/generate/qr", GenerateQR.as_view(), name='qr-generate'),
    path("api/admins/download/qr", DownloadQR.as_view(), name='qr-download'),

    path("api/menu/thumb/<int:pk>", menu_view.UpdatePhotoMenu.as_view({"put": "update", "get": "retrieve"}), name='update-photo'),

    
    # new routes
    path("api/v1/", include(router.urls)),
] 

# urlpatterns+=adminpatterns
# urlpatterns+=clientpatterns
