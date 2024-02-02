from django.urls import include, path
from menu_app.admins.urls import urlpatterns as adminpatterns
from menu_app.clients.urls import urlpatterns as clientpatterns
from menu_app.admins.router import *
from menu_app.clients.router import *



urlpatterns = [
    path("api/admins/", include("menu_app.admins.urls")),
    path("api/client/", include("menu_app.clients.urls")),
    
] 

# urlpatterns+=adminpatterns
# urlpatterns+=clientpatterns
