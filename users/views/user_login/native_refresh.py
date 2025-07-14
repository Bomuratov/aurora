from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.models import User
from users.exceptions.authentication_error import AuthenticationErrorException
from users.views.docs.user_token_docs import docs


@extend_schema_view(
    post=extend_schema(tags=docs.tags, description=docs.description.refresh)
)
class UserNativeRefreshView(views.TokenRefreshView):

    def post(self, request, *args, **kwargs):
        raw_token = request.data.get("refresh")
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

        if str(user.role) == "is_courier":
            new_refresh = tokens.RefreshToken.for_user(user)
            restaurant = user.editors.first()

            access = new_refresh.access_token
            access["email"] = user.email
            access["is_user"] = user.is_user
            access["is_vendor"] = user.is_vendor
            access["vendor"] = str(restaurant) if restaurant else None
            access["role"] = str(user.role)

            return response.Response(
                {
                    "access": str(access),
                    "refresh": str(new_refresh),
                    "access_expires": access.payload["exp"],
                    "refresh_expires": new_refresh.payload["exp"],
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {
                "message": "Вы не являетесь курьером ни в одном ресторане за подробностями обратитесь к ресторану",
                "code": 3,
            },
            status=status.HTTP_403_FORBIDDEN,
        )
