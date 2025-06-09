from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from menu_app.view import variant_view

urlpatterns = [

    # default urls
    path("admin/", admin.site.urls),
    path('api/auth/', include("rest_framework.urls")),
    
    # swagger urls
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api/v1/script", variant_view.create_option_group, name="menu-variant"),

    # apllication urls
    path("", include(("menu_app.urls", "core"), namespace="menu_app")),
    path("api/v1/", include([
        path("auth/", include("users.urls")),
   ])),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()



