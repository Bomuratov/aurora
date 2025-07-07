from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from menu_app.models import DeliveryRule


class DeliveryCalculationView(APIView):
    def get(self, request):
        restaurant_id = request.query_params.get("vendor_id")
        order_price = request.query_params.get("order_cost")
        distance = request.query_params.get("distance")

        if not all([restaurant_id,order_price, distance]):
            return Response(
                {"message": "Не передан один из обязательных параметров", "code": 4},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order_price = float(order_price)
            distance = float(distance) if distance else 0
        except ValueError:
            return Response(
                {"message": "Некорректный тип параметров", "code": 4},
                status=status.HTTP_400_BAD_REQUEST
            )

        rule = DeliveryRule.objects.filter(
            restaurant_id=restaurant_id, is_active=True
        ).first()

        if not rule:
            return Response(
                {"message": "Активное правило не найдено", "code": 4},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if rule.reverse_calculate:
            if order_price <= rule.max_order_price_for_free_delivery:
                return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})
            
        if rule.reverse_calculate == False:
            if rule.max_order_price_for_free_delivery and \
            order_price >= rule.max_order_price_for_free_delivery:
                return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})

        if rule.calculation_type == "per_km":
            result = rule.price_per_km * distance
            return Response({"message": f"Сумма доставки {result} UZS", "price": result, "code": 2})

        if rule.calculation_type == "percent":
            result = round(order_price * rule.price_per_percent / 100)
            return Response({"message": f"Сумма доставки {result} UZS", "price": result, "code": 3})

        return Response(
            {"message": "Такое правило пока не поддерживается", "code": 4},
            status=status.HTTP_400_BAD_REQUEST
        )
