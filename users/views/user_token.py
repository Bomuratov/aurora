from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers.user_token import UserTokenSerializer


class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer