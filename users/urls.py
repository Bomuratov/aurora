from django.urls import path
from users.views import register, user_token, user_view, vendor_register, user_location_view, user_settings_view
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register", register.UserRegisterView.as_view({"post":"create"}), name="register"),
    
    path("vendor/register", vendor_register.VendorRegisterView.as_view({"post":"create"}), name="register"),

    path("user/", user_view.UserView.as_view({"get":"list"}), name="user-list"),
    path("user/<int:pk>", user_view.UserView.as_view({"get":"retrieve"}), name="user-get"),
    path("user/<int:pk>/", user_view.UserView.as_view({"put":"update"}), name="user-update"),

    # LOGIN FOR NATIVE MOBILE 
    path("native/login", user_token.UserTokenView.as_view(), name="user-login"),
    path("native/refresh", user_token.RefreshTokenView.as_view(), name="refresh-token"),

    # HTTPONLY COOKIE LOGIN APIS
    path("user/login", user_token.UserTokensView.as_view(), name="user-login"),
    path("refresh", user_token.RefreshTokensView.as_view(), name="refresh-token"),

    # User location CRUD's
    path("user/location", user_location_view.UserLocationView.as_view({"get": "list", "post": "create"}), name="user-location"),
    path("user/location/<int:pk>", user_location_view.UserLocationView.as_view({"put": "update", "delete": "destroy"}), name="user-location-update"),
    path("user/location/<int:pk>/toggle_active", user_location_view.UserLocationView.as_view({"patch": "toggle_active"}), name="user-location-toggle"),

    path("user/channel/", user_settings_view.UserSettingsView.as_view({"get": "list",}), name="user-channel"),
    path("user/channel/<int:pk>", user_settings_view.UserSettingsView.as_view({"patch": "update_token"}), name="user-update"),



]


