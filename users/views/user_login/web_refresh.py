from datetime import timedelta
from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from users.exceptions.authentication_error import AuthenticationErrorException
from django.middleware.csrf import get_token
from menu_app.models import Restaurant
from users.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.views.docs.user_token_docs import docs, web_docs


@extend_schema_view(
    post=extend_schema(tags=web_docs.tags, description=web_docs.description.refresh)
)
class CookieUserRefreshView(views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get("refresh_token")
        if not raw_token:
            raise AuthenticationErrorException(
                "Токен недействителен или просрочен", code=4
            )

        try:
            old_refresh = tokens.RefreshToken(token=raw_token)
        except Exception:
            raise AuthenticationErrorException(
                "Данный токен ранее использовань.", code=3
            )

        if settings.SIMPLE_JWT["BLACKLIST_AFTER_ROTATION"]:
            try:
                old_refresh.blacklist()
            except AttributeError:
                pass

        user_id = old_refresh["user_id"]
        user = User.objects.filter(id=user_id).first()
        new_refresh = tokens.RefreshToken.for_user(user)
        # vendor = list(user.editors.all().values_list("name", flat=True))
        vendor = user.editors.all().first()
        
        access = new_refresh.access_token
        access["is_user"] = user.is_user
        access["is_vendor"] = user.is_vendor
        access["vendor"] = str(vendor) if vendor else None
        access["role"] = str(user.role)

        responce = response.Response(
            {
                "access_token": str(access),
                "access_expires": access.payload["exp"],
                "refresh_expires": new_refresh.payload["exp"],
            },
            status=status.HTTP_200_OK,
        )

        responce.set_cookie(
            "refresh_token",
            str(new_refresh),
            max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
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