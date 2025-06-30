from rest_framework import response, viewsets, decorators, status
from menu_app.models import DeliveryRule, Restaurant
from menu_app.serializer.delivery_rule_serializer import DeliveryRuleSerializer
from users.models import UserLocation


class DeliveryRuleView(viewsets.ModelViewSet):
    queryset = DeliveryRule.objects.all()
    serializer_class = DeliveryRuleSerializer
    lookup_field = "pk"

    @decorators.action(detail=True, methods=["get"])
    def get_delivery_info(self, request, pk=None):
        restaurant_id = request.query_params.get("restaurant_id")
        user_id = request.query_params.get("user_id")

        if not restaurant_id or not user_id:
            return response.Response(
                {"message": "Параметры 'restaurant_id' и 'user_id' обязательны.", "code": 4},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            restaurant_id = int(restaurant_id)
            user_id = int(user_id)
        except (ValueError, TypeError):
            return response.Response(
                {"message": "Параметры должны быть числами.", "code": 4},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery_rule = (
            DeliveryRule.objects
            .select_related("restaurant")
            .filter(restaurant_id=restaurant_id, is_active=True)
            .only(
                "id", "calculation_type", "min_distance", "max_distance",
                "fixed_price", "price_per_km", "price_per_percent",
                "restaurant__id", "restaurant__lat", "restaurant__long"
            )
            .first()
        )

        if not delivery_rule:
            return response.Response(
                {"message": "Правила доставки не найдены.", "code": 5},
                status=status.HTTP_404_NOT_FOUND
            )

        user_location = (
            UserLocation.objects
            .filter(user_id=user_id, is_active=True)
            .only("lat", "long")
            .first()
        )

        if not user_location:
            return response.Response(
                {"message": "Локация пользователя не найдена.", "code": 5},
                status=status.HTTP_404_NOT_FOUND
            )

        restaurant = delivery_rule.restaurant

        return response.Response({
            "user": {
                "location": {
                    "lat": user_location.lat,
                    "long": user_location.long
                }
            },
            "restaurant": {
                "location": {
                    "lat": restaurant.lat,
                    "long": restaurant.long
                }
            },
            "delivery_type": delivery_rule.calculation_type,
            "delivery_rule": self.get_serializer(delivery_rule).data
        })
