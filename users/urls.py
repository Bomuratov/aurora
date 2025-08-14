from django.urls import path
from users.views import register, user_view, vendor_register, user_location_view, user_settings_view, user_role_views
from users.views.user_login import native_login, native_refresh, web_login, web_refresh, user_native_login, user_native_refresh


urlpatterns = [
    path("register", register.UserRegisterView.as_view({"post":"create"}), name="user-register"),
    
    path("vendor/register", vendor_register.VendorRegisterView.as_view({"post":"create"}), name="vendor-register"),

    path("user/", user_view.UserView.as_view({"get":"list"}), name="user-get-list"),
    path("user/me", user_view.UserView.as_view({"get":"me"}), name="user-me-list"),
    path("user/<int:pk>", user_view.UserView.as_view({"get":"retrieve"}), name="user-me"),
    path("user/<int:pk>/", user_view.UserView.as_view({"put":"update"}), name="user-update"),

    # LOGIN FOR NATIVE APPLICATIONS 
    path("native/login", native_login.UserNativeLoginView.as_view(), name="user-native-login"),
    path("native/refresh", native_refresh.UserNativeRefreshView.as_view(), name="refresh-token-native"),

    # LOGIN FOR USER NATIVE APPLICATIONS
    path("user/native/login", user_native_login.NativeUserLogin.as_view(), name="user-native-login"),
    path("user/native/refresh", user_native_refresh.UserNativeRefreshView.as_view(), name="refresh-token-native"),

    # HTTPONLY COOKIE LOGIN API'S FOR WEB LOGIN
    path("user/login", web_login.CookieUserWebLoginView.as_view(), name="user-web-login"),
    path("refresh", web_refresh.CookieUserRefreshView.as_view(), name="refresh-token-web"),

    # USER LOCATION CRUD'S
    path("user/location", user_location_view.UserLocationView.as_view({"get": "list", "post": "create"}), name="user-location"),
    path("user/location/<int:pk>", user_location_view.UserLocationView.as_view({"put": "update", "delete": "destroy"}), name="user-location-update"),
    path("user/location/<int:pk>/toggle_active", user_location_view.UserLocationView.as_view({"patch": "toggle_active"}), name="user-location-toggle"),

    # USER FCM TOKEN CRUD'S
    path("user/channel/", user_settings_view.UserSettingsView.as_view({"get": "list",}), name="user-channel"),
    path("user/channel/<int:pk>", user_settings_view.UserSettingsView.as_view({"patch": "update_token"}), name="user-channel-update"),

    # USER ROLES CRUD
    path("user/role-labels", user_role_views.get_role_labels, name="get-roles-labels"),
    path("user/roles", user_role_views.UserRoleView.as_view({"get": "list", "post": "create"}), name="user-role-get-create"),
    path("user/roles/<int:pk>", user_role_views.UserRoleView.as_view({"put": "update", "delete": "destroy"}), name="user-role-update-delete"),
    



]


