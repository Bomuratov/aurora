from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from users.serializers.user_token import UserTokenSerializer
from rest_framework_simplejwt.views import TokenRefreshView



@extend_schema(tags=["User login API"])
class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer


@extend_schema(tags=["User login API"])
class RefreshTokenView(TokenRefreshView):
    pass

