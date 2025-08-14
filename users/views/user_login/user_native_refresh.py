from rest_framework import status, response
from rest_framework_simplejwt import views, tokens
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.models import User
from users.exceptions.authentication_error import AuthenticationErrorException
from users.views.docs.user_token_docs import native_docs


@extend_schema_view(
    post=extend_schema(tags=native_docs.tags, description=native_docs.description.refresh)
)
class UserNativeRefreshView(views.TokenRefreshView):
    pass