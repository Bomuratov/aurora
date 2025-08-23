from rest_framework import viewsets, permissions, views, response, decorators
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from menu_app.models import Restaurant, Schedule
from menu_app.serializer.restaurant_serializer import (
    RestaurantSerializer,
    RestaurantChannels,
    RestaurantEditors,
    RestaurantCouriersSerializer,
)
from menu_app.view.docs.restaurant_view_docs import docs
from django.utils import timezone
from datetime import datetime
import datetime as dt
from users.permissions.role_checks import RoleCheck


@extend_schema_view(
    list=extend_schema(tags=docs.tags, description=docs.description.get_list),
    retrieve=extend_schema(tags=docs.tags, description=docs.description.get_retrieve),
    create=extend_schema(tags=docs.tags, description=docs.description.create),
    update=extend_schema(tags=docs.tags, description=docs.description.update),
    partial_update=extend_schema(
        tags=docs.tags, description=docs.description.partial_update
    ),
    destroy=extend_schema(tags=docs.tags, description=docs.description.destroy),
)
class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes=[RoleCheck]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("user_id", "name", "id")
    lookup_field = "name"
    permission_classes = [permissions.AllowAny]

    @decorators.action(methods=["GET"], detail=False)
    def get_restaurant_by_id(self, request, pk):
        obj = self.get_queryset().get(id=pk)
        serializer = self.get_serializer(obj)
        return response.Response(serializer.data)



@extend_schema_view(
    list=extend_schema(tags=docs.tags, description=docs.description.get_channel_pm),
    retrieve=extend_schema(tags=docs.tags, description=docs.description.get_channel),
)
class RestaurantChannelsView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantChannels
    permission_classes=[RoleCheck]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("user_id", "id")
    lookup_field = "pk"


@extend_schema_view(
    retrieve=extend_schema(tags=docs.tags, description=docs.description.get_editors),
)
class RestaurantEditorsView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantEditors
    permission_classes=[RoleCheck]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id", "name")
    lookup_field = "pk"


@extend_schema_view(
    retrieve=extend_schema(tags=docs.tags, description=docs.description.get_editors),
)
class RestaurantCouriersView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCouriersSerializer
    permission_classes=[RoleCheck]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id", "name")
    lookup_field = "pk"

    @decorators.action(methods=["GET"], detail=True)
    def get_restaurant_couriers(self, request, pk):
        instance = self.get_object()
        couriers = instance.editors.filter(role__role="is_courier")
        couriers_list = []

        for courier in couriers:
            couriers_list.append(
                {
                    "id": courier.id,
                    "full_name": f"{courier.first_name} {courier.last_name}",
                    "role": courier.role.role if courier.role else None,  # если role это FK
                    "is_active": courier.is_active,
                }
            )
        return response.Response(couriers_list)


class RestaurantStatusView(views.APIView):
    def get(self, request, pk):
        now = timezone.localtime()
        current_time = now.time()
        current_weekday = now.weekday()
        next_weekday = (current_weekday + 1) % 7
        schedules_today = Schedule.objects.filter(restaurant_id=pk, day=current_weekday)
        schedules_yesterday = Schedule.objects.filter(
            restaurant_id=pk, day=next_weekday
        )
        is_open = False

        if not schedules_today:
            return response.Response(
                {"is_open": True, "message": "График не указан", "code": 4}
            )

        for schedule in schedules_today:
            open_time = schedule.open_time
            close_time = schedule.close_time
            if open_time < close_time:
                if open_time <= current_time <= close_time:
                    is_open = True
                    break
            else:
                if current_time >= open_time or current_time <= close_time:
                    is_open = True
                    break

        if not is_open:
            for schedule in schedules_yesterday:
                open_time = schedule.open_time
                close_time = schedule.close_time

                if open_time > close_time:
                    if current_time <= close_time:
                        is_open = True
                        break

        return response.Response(
            {
                "is_open": is_open,
                "message": "Открыто." if is_open else "Закрыто.",
                "code": 1 if is_open else 0,
            }
        )
