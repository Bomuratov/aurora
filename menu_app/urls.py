from django.urls import include, path
from menu_app.admins.urls import urlpatterns as adminpatterns
from menu_app.clients.urls import urlpatterns as clientpatterns
from menu_app.admins.router import *
from menu_app.clients.router import *
from menu_app.utils import GenerateQR, DownloadQR



urlpatterns = [
    path("api/admins/", include("menu_app.admins.urls")),
    path("api/client/", include("menu_app.clients.urls")),
    path('api/admins/categories/update_order/', CategoryView.as_view({'post': 'post_update'}), name='category_update_order'),
    path("api/admins/generate/qr", GenerateQR.as_view(), name='qr-generate'),
    path("api/admins/download/qr", DownloadQR.as_view(), name='qr-download'),
    
] 

# urlpatterns+=adminpatterns
# urlpatterns+=clientpatterns
