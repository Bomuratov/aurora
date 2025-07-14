from datetime import timedelta
from django.contrib.auth import login
from django.middleware.csrf import get_token
from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from users.serializers.user_token import UserTokenSerializer
from users.exceptions.authentication_error import AuthenticationErrorException
from users.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.views.docs.user_token_docs import docs, web_docs


@extend_schema_view(
    post=extend_schema(tags=web_docs.tags, description=web_docs.description.access)
)
class CookieUserWebLoginView(views.TokenObtainPairView):
    serializer_class = UserTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise AuthenticationErrorException(
                detail="Логин или пароль не верный", code=4
            )

        user = serializer.user
        login(request, user)
        refresh = tokens.RefreshToken.for_user(user)
        access_token = refresh.access_token
        # vendor = list(user.editors.all().values_list("name", flat=True))
        vendor = user.editors.all().first()
        access_token["is_user"] = user.is_user
        access_token["is_vendor"] = user.is_vendor
        access_token["vendor"] = str(vendor) if vendor else None
        access_token["role"] = str(user.role)
        access_token = str(access_token)
        refresh_token = str(refresh)
        responce = response.Response(
            {
                "access_token": access_token,
                "access_expires": refresh.access_token.payload["exp"],
                "refresh_expires": refresh.payload["exp"],
            },
            status=status.HTTP_200_OK,
        )

        responce.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        csrf = get_token(request)
        responce.set_cookie(
            "csrftoken",
            csrf,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
        )
        return responce
