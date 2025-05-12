from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from users.serializers.user_token import UserTokenSerializer
from users.exceptions.authentication_error import AuthenticationErrorException
from menu_app.models import Restaurant
from datetime import timedelta
from django.contrib.auth import login
from django.middleware.csrf import get_token
from users.models import User
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["User login API NATIVE"])
class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer


@extend_schema(tags=["User login API NATIVE"])
class RefreshTokenView(TokenRefreshView):
    pass

# @method_decorator(csrf_exempt, name='dispatch')
@extend_schema(tags=["USER WEB LOGIN API"])
class CookieUserTokensView(TokenObtainPairView):
    serializer_class = UserTokenSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise AuthenticationErrorException(detail="Логин или пароль не верный", code=4)
 
        user = serializer.user
        login(request, user)
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
            "refresh_expires": refresh.payload['exp']
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

        csrf = get_token(request)
        response.set_cookie(
            "csrftoken",
            csrf,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
        )
        return response




# class CookieRefreshTokensView(TokenRefreshView):

#     def post(self, request, *args, **kwargs):
#         refresh_token = request.COOKIES.get("refresh_token")
#         print(request.user)
#         if not refresh_token:
#             raise AuthenticationErrorException(detail="Токен недействителен или просрочен", code=4)
#         try:
#             old_refresh = RefreshToken(refresh_token)
#             user_id = old_refresh["user_id"]
#             new_refresh = RefreshToken()
#             new_refresh["user_id"] = user_id
#             access_token = new_refresh.access_token
#             user = get_object_or_404(User, pk=user_id)
#             restaurant = Restaurant.objects.filter(user_id=user_id).first()
#             access_token["email"] = user.email
#             access_token["is_user"] = user.is_user
#             access_token["is_vendor"] = user.is_vendor
#             access_token["vendor"] = str(restaurant) if restaurant else None
#         except Exception:
#             raise AuthenticationErrorException(detail="Токен недействителен или просрочен", code=3)
        
#         response = Response({
#             "access_token": str(access_token),
#             "access_expires": access_token.payload['exp'],
#             "refresh_expires": new_refresh.payload['exp'],
#         }, status=HTTP_200_OK)

#         response.set_cookie(
#             key="refresh_token",
#             value=new_refresh,
#             max_age=int(timedelta(days=1).total_seconds()),
#             httponly=True,
#             secure=True,
#             samesite="None",
#             path="/",
#         )
#         csrf = get_token(request)
#         response.set_cookie(
#             "csrftoken",
#             csrf,
#             max_age=int(timedelta(days=7).total_seconds()),
#             httponly=False,
#             secure=True,
#             samesite="None",
#             path="/",
#         )

#         return response


@extend_schema(tags=["USER WEB LOGIN API"])
class CookieRefreshTokensView(TokenRefreshView):
    """
    Кастомная версия TokenRefreshView, 
    но с ротацией + черным списком старых токенов
    """

    def post(self, request, *args, **kwargs):
        raw_token = request.COOKIES.get("refresh_token")
        if not raw_token:
            raise AuthenticationErrorException("Токен недействителен или просрочен", code=4)

        try:
            # 1) Декодим старый токен (валидация подписи, срока жизни)
            old_refresh = RefreshToken(raw_token)
        except Exception:
            raise AuthenticationErrorException("Токен недействителен или просрочен", code=3)

        # 2) Чёрный список (если включена опция BLACKLIST_AFTER_ROTATION)
        if settings.SIMPLE_JWT["BLACKLIST_AFTER_ROTATION"]:
            try:
                # Сохраняем старый токен в таблице черных
                old_refresh.blacklist()
            except AttributeError:
                # если модель BlacklistedToken не подхватили
                pass

        # 3) Генерируем новый refresh через for_user() — это гарантированно
        #    создаст правильный JTI, exp и сделает запись OutstandingToken
        user_id = old_refresh["user_id"]
        user = get_object_or_404(User, pk=user_id)
        new_refresh = RefreshToken.for_user(user)

        # 4) Собираем новый access и доп. claim'ы
        access = new_refresh.access_token
        # ваши дополнительные поля
        access["email"]       = user.email
        access["is_user"]     = user.is_user
        access["is_vendor"]   = user.is_vendor
        access["vendor"]      = str(Restaurant.objects.filter(user_id=user_id).first() or "")

        # 5) Отдаём их в Response и в куки
        response = Response({
            "access_token": str(access),
            "access_expires":   access.payload["exp"],
            "refresh_expires":  new_refresh.payload["exp"],
        }, status=HTTP_200_OK)

        # Положим новый refresh в httponly-куку
        response.set_cookie(
            "refresh_token",
            str(new_refresh),
            max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )
        # Обновим CSRF-токен
        csrf = get_token(request)
        response.set_cookie(
            "csrftoken",
            csrf,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=False,
            secure=True,
            samesite="None",
            path="/",
        )
        return response
