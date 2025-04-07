from django.urls import path
from users.views import register, user_token, user_view, vendor_register



urlpatterns = [
    path("register", register.UserRegisterView.as_view({"post":"create"}), name="register"),
    
    path("vendor/register", vendor_register.VendorRegisterView.as_view({"post":"create"}), name="register"),

    path("user/", user_view.UserView.as_view({"get":"list"}), name="user-list"),
    path("user/<int:pk>", user_view.UserView.as_view({"get":"retrieve"}), name="user-get"),
    path("user/<int:pk>/", user_view.UserView.as_view({"put":"update"}), name="user-update"),

    path("user/login", user_token.UserTokenView.as_view(), name="user-login"),
    path("refresh", user_token.RefreshTokenView.as_view(), name="refresh-token"),
]


