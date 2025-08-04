from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from menu_app.models import DeliveryRule


class DeliveryCalculationView(APIView):
    def get(self, request):
        restaurant_id = request.query_params.get("vendor_id")
        order_price = request.query_params.get("order_cost")
        distance = request.query_params.get("distance")

        if not all([restaurant_id, order_price, distance]):
            return Response(
                {"message": "Не передан один из обязательных параметров", "code": 4},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order_price = float(order_price)
            distance = float(distance) if distance else 0
        except ValueError:
            return Response(
                {"message": "Некорректный тип параметров", "code": 4},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rule = DeliveryRule.objects.filter(
            restaurant_id=restaurant_id, is_active=True
        ).first()

        if not rule:
            return Response(
                {"message": "Активное правило не найдено", "code": 4},
                status=status.HTTP_404_NOT_FOUND,
            )

        if rule.reverse_calculate or rule.reverse_calculate:
            if order_price <= rule.max_order_price_for_free_delivery:
                return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})

        if rule.reverse_calculate == False:
            if (
                rule.max_order_price_for_free_delivery
                and order_price >= rule.max_order_price_for_free_delivery
            ):
                return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})

        if rule.calculation_type == "per_km":
            result = rule.price_per_km * distance
            return Response(
                {
                    "message": f"Сумма доставки {round(result)} UZS",
                    "price": round(result),
                    "code": 2,
                }
            )

        if rule.calculation_type == "percent":
            result = round(order_price * rule.price_per_percent / 100)
            return Response(
                {
                    "message": f"Сумма доставки {round(result)} UZS",
                    "price": round(result),
                    "code": 3,
                }
            )

        if rule.calculation_type == "fixed":
            return Response(
                {
                    "message": f"Сумма доставки {round(rule.fixed_price)} UZS",
                    "price": round(rule.fixed_price),
                    "code": 2,
                }
            )

        return Response(
            {"message": "Такое правило пока не поддерживается", "code": 4},
            status=status.HTTP_400_BAD_REQUEST,
        )


# class DeliveryCalculationView(APIView):
#     def get(self, request):
#         restaurant_id = request.query_params.get("vendor_id")
#         order_price = request.query_params.get("order_cost")
#         distance = request.query_params.get("distance")

#         if not all([restaurant_id,order_price, distance]):
#             return Response(
#                 {"message": "Не передан один из обязательных параметров", "code": 4},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             order_price = float(order_price)
#             distance = float(distance) if distance else 0
#         except ValueError:
#             return Response(
#                 {"message": "Некорректный тип параметров", "code": 4},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         delivery_rule = DeliveryRule.objects.filter(
#             restaurant_id=restaurant_id, is_active=True
#         )

#         rule_km_or_percent = delivery_rule.filter(calculation_type__in=["per_km", "percent"]).first()
#         rule_fixed = delivery_rule.filter(calculation_type = "fixed")

#         # проверка на наличие правило доставки
#         if not rule_km_or_percent and not rule_fixed:
#             return Response(
#                 {"message": "Активное правило не найдено", "code": 4},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if rule_km_or_percent:
#             # подсчет бесплатной доставки в случае reverse_calculate=True
#             if rule_km_or_percent.reverse_calculate:
#                 if order_price <= rule_km_or_percent.max_order_price_for_free_delivery:
#                     return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})

#             # подсчет бесплатной доставки в случае reverse_calculate=False
#             if rule_km_or_percent.reverse_calculate == False:
#                 if rule_km_or_percent.max_order_price_for_free_delivery and \
#                 order_price >= rule_km_or_percent.max_order_price_for_free_delivery:
#                     return Response({"message": "Сумма доставки 0", "price": 0, "code": 0})


#             # подсчет по километражу
#             if rule_km_or_percent.calculation_type == "per_km":
#                 result = rule_km_or_percent.price_per_km * distance
#                 return Response({"message": f"Сумма доставки {round(result)} UZS", "price": round(result), "code": 2})

#             # подсчет по пронценту от суммы заказа
#             if rule_km_or_percent.calculation_type == "percent":
#                 result = round(order_price * rule_km_or_percent.price_per_percent / 100)
#                 return Response({"message": f"Сумма доставки {round(result)} UZS", "price": round(result), "code": 3})


#         # подсчет по фикс цене
#         rule_in_range = rule_fixed.filter(min_distance__lte=distance, max_distance__gte=distance).first()
#         if rule_in_range:
#             return Response({
#                 "message": f"Сумма доставки {rule_in_range.fixed_price} UZS",
#                 "price": rule_in_range.fixed_price,
#                 "code": 2
#             })

#         # Если ни одно правило не подошло — ищем ближайшее максимальное
#         rule_fallback = rule_fixed.order_by('-max_distance').first()
#         if rule_fallback:
#             return Response({
#                 "message": f"Сумма доставки {rule_fallback.fixed_price} UZS",
#                 "price": rule_fallback.fixed_price,
#                 "code": 2
#             })


#         # if rule.calculation_type == "fixed":
#         #     return Response({"message": f"Сумма доставки {round(rule.fixed_price)} UZS", "price": round(rule.fixed_price), "code": 2})

#         return Response(
#             {"message": "Такое правило пока не поддерживается", "code": 4},
#             status=status.HTTP_400_BAD_REQUEST
#         )
