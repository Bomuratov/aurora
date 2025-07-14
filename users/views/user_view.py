from rest_framework import viewsets, views, response, permissions, decorators, status
from drf_spectacular.utils import extend_schema_view, extend_schema
from users.models import User
from users.serializers.user_serializer import UserSerializer
from users.views.docs.user_docs import docs

@extend_schema_view(
    list=extend_schema(
        tags=docs.tags,
        description=docs.description.get_list
    ),
    retrieve=extend_schema(
        tags=docs.tags,
        description=docs.description.get_retrieve
    ),
    update=extend_schema(
        tags=docs.tags,
        description=docs.description.update
    ),
    me=extend_schema(
        tags=docs.tags,
        description=docs.description.me
    ),
)
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    @decorators.action(methods=["GET"], detail=False)
    def me(self, request):
        user = request.user
        if not user.is_authenticated:
            print("proshli")
            return response.Response({"message": "Вы не зарегистрированы", "code": 4}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(user)
        return response.Response(serializer.data)