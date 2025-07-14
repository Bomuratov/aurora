from datetime import timedelta
from django.contrib.auth import login
from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.models import User
from users.serializers.user_token import UserTokenSerializer
from users.exceptions.authentication_error import AuthenticationErrorException
from users.views.docs.user_token_docs import docs, web_docs


@extend_schema_view(
    post=extend_schema(tags=docs.tags, description=docs.description.access)
)
class UserNativeLoginView(views.TokenObtainPairView):
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
        print(user.role)

        if str(user.role) == "is_courier":
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
            return response.Response(
                {
                    "access": access_token,
                    "refresh": refresh_token,
                    "access_expires": refresh.access_token.payload["exp"],
                    "refresh_expires": refresh.payload["exp"],
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
