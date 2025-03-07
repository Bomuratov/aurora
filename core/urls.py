from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from menu_app.views import CustomTokenObtain

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include("rest_framework.urls")),

    path(
        "api_schema/",
        get_schema_view(title="API Schema", description="Guide for the REST API"),
        name="api_schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="docs.html", extra_context={"schema_url": "api_schema"}
        ),
        name="swagger-ui",
    ),
    path("", include(("menu_app.urls", "core"), namespace="menu_app")),
    path("api/v1/", include([
        path("auth/", include("users.urls")),
   ])),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
