from django.urls import  path, include
from menu_app.admins.api import *
from menu_app.admins.router import *



urlpatterns = [
    path("", include(adminrouter.urls)),

    # Api Category
    path("category/<str:restaurant_name>", CategoryAdminView.as_view({"get":"list"}), name="category"),




    # Api Menu
    path("menu/<str:restaurant_name>", MenuAdminView.as_view({"get":"list"}), name="menu"),



    # Api Promo
    path("promo/<str:restaurant_name>", PromoAdminView.as_view({"get":"list"}), name="promo"),
    
]