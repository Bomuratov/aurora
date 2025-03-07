from django.urls import path
from users.views.register import UserRegisterView


urlpatterns = [
    path("register", UserRegisterView.as_view({"post":"create"}), name="register"),
    path("user", UserRegisterView.as_view({"get":"list"}), name="user-list"),
    path("user/<int:pk>", UserRegisterView.as_view({"get":"retrieve"}), name="user-get"),
    path("user/<int:pk>", UserRegisterView.as_view({"put":"update"}), name="user-update"),
    path("user/<int:pk>", UserRegisterView.as_view({"delete":"destroy"}), name="user-delete"),
]