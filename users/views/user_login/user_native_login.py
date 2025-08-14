from datetime import timedelta
from django.contrib.auth import login
from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.models import User
from users.serializers.user_token import UserTokenSerializer
from users.exceptions.authentication_error import AuthenticationErrorException
from users.views.docs.user_token_docs import native_docs

@extend_schema_view(
    post=extend_schema(tags=native_docs.tags, description=native_docs.description.access)
)
class NativeUserLogin(views.TokenObtainPairView):
    serializer_class = UserTokenSerializer
