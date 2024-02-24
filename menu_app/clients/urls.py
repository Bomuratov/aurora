from django.urls import path, include
from menu_app.clients.api import *
from menu_app.clients.router import *



urlpatterns = [
    path("", include(clientrouter.urls)),

    # API Restaurant
    path("restaurant/<str:name>", RestaurantClientView.as_view({'get': 'retrieve'}), name="restaurant-get"),
    
    
    # API Category
    path("category/<str:restaurant_name>", CategoryClientView.as_view({"get":"list"}), name="category"),


    # API Menu
    path("menu/<str:restaurant_name>", MenuClientView.as_view({"get":"list"}), name="menu"),


    # API Promo
    path("promo/<str:restaurant_name>", PromoClientView.as_view({"get":"list"}), name="promo"),

]
