from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from users.serializers.user_token import UserTokenSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from users.exceptions.authentication_error import AuthenticationErrorException
from menu_app.models import Restaurant
from datetime import timedelta, datetime



@extend_schema(tags=["User login API NATIVE"])
class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer


@extend_schema(tags=["User login API NATIVE"])
class RefreshTokenView(TokenRefreshView):
    pass


# @method_decorator(csrf_exempt, name='dispatch')
class CookieUserTokensView(TokenObtainPairView):
    serializer_class = UserTokenSerializer

    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise AuthenticationErrorException(detail="Логин или пароль не верный", code=4)

 
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        restaurant = Restaurant.objects.filter(user_id=user.id).first()
        access_token["email"] = user.email
        access_token["is_user"] = user.is_user
        access_token["is_vendor"] = user.is_vendor
        access_token["vendor"] = str(restaurant) if restaurant else None
        access_token = str(access_token)
        refresh_token = str(refresh)
        response = Response({
            "access_token": access_token,
            "access_expires": refresh.access_token.payload['exp'],
            "refresh_expires": refresh.payload['exp'],
        }, status=HTTP_200_OK)


        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )
        return response


class CookieRefreshTokensView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            raise AuthenticationErrorException(detail="Токен недействителен или просрочен", code=4)
        try:
            old_refresh = RefreshToken(refresh_token)
            user_id = old_refresh["user_id"]
            new_refresh = RefreshToken()
            new_refresh["user_id"] = user_id
            access_token = new_refresh.access_token
        except Exception:
            raise AuthenticationErrorException(detail="Токен недействителен или просрочен", code=3)
        
        response = Response({
            "access_token": str(access_token),
            "access_expires": access_token.payload['exp'],
            "refresh_expires": new_refresh.payload['exp'],
        }, status=HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh,
            max_age=int(timedelta(days=1).total_seconds()),
            httponly=True,
            secure=True,
            samesite="Lax",
            path="/",
        )

        return response
