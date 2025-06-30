from rest_framework import viewsets, decorators, response
from users.models import UserSettings
from users.serializers.user_settings_serializer import UserSettingsSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.views.docs.user_settings_docs import docs


@extend_schema_view(
    list=extend_schema(
        tags=docs.tags,
        description=docs.description.list
    ),
    update_token=extend_schema(
        tags=docs.tags,
        description=docs.description.update
    ),
)

class UserSettingsView(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    lookup_field = "pk"

    @decorators.action(detail=True, methods=["PATCH"])
    def update_token(self, request, pk=None):
        instance = self.get_object()
        fcm_token = request.data.get("fcm_token", None)
        device_type = request.data.get("device_type", None)
        device_model = request.data.get("device_model", None)
        instance.fcm_token = fcm_token
        instance.device_type = device_type
        instance.device_model = device_model
        instance.save()
        return response.Response({"message": "fcm_token добавлен", "code": 2})
