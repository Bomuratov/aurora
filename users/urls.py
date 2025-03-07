from django.urls import path
from users.views import register, user_token
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register", register.UserRegisterView.as_view({"post":"create"}), name="register"),
    path("user", register.UserRegisterView.as_view({"get":"list"}), name="user-list"),
    path("user/<int:pk>", register.UserRegisterView.as_view({"get":"retrieve"}), name="user-get"),
    path("user/<int:pk>", register.UserRegisterView.as_view({"put":"update"}), name="user-update"),
    path("user/<int:pk>", register.UserRegisterView.as_view({"delete":"destroy"}), name="user-delete"),
    path("user/login", user_token.UserTokenView.as_view(), name="user-login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh-token"),
]


