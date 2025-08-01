from rest_framework import views, response
from users.serializers.register import OtpCodeSerializer
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import random


class SendOtpView(views.APIView):
    def post(self, request):
        serializer = OtpCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_data = serializer.save()
        # тут будем отправить смс на номер пользователя
        # send_otp(phone=serializer.validated_data['phone'], code=otp_data['code'], code_expiry=otp_data['code_expiry'])
        return response.Response(
            {
                "message": "OTP успешно отправлен.",
                "phone": serializer.validated_data["phone"],
                "code": otp_data["code"],
                "code_expiry": otp_data["code_expiry"],
                "max_code_try": otp_data["max_code_try"],
                "code_max_out": otp_data["code_max_out"],
            }
        )


class VerifyOtpView(views.APIView):

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")

        if not phone and code:
            return response.Response(
                {"message": "Не передан номер телефона или код подтверждения"}
            )

        otp_data = cache.get(key=f"otp:{phone}")
        if not otp_data:
            return response.Response(
                {"message": "Код подтверждения просрочен или не найден"}
            )

        if timezone.now() >= otp_data["code_expiry"]:
            return response.Response({"message": "Код подтверждения просрочен"})

        if int(code) != int(otp_data["code"]):
            return response.Response({"message": "Введённый код неправильно"})
        
        cache.delete(key=f"otp:{phone}")
        return response.Response({"message": "Номер телефона успешно подтверждена"})



class RegenerateOtpView(views.APIView):
    def post(self, request):
        local_time = timezone.localtime(timezone.now())
        phone = request.data.get("phone")

        if not phone:
            return response.Response(
                {"message": "Не передан номер телефона или код подтверждения"}
            )

        otp_data = cache.get(key=f"otp:{phone}")

        if not otp_data:
            return response.Response(
                {"message": "Код подтверждения просрочен или не найден"}
            )

        if otp_data["max_code_try"] == 0:
            otp_data["max_code_try"] = 5
            otp_data["code_max_out"] = local_time + timedelta(minutes=11)
            cache.set(key=f"otp:{phone}", value=otp_data)
            return response.Response(
                {"message": "Вы много раз запросили код попробуйте через 10 мин",
                 "data": {
                    "phone": phone,
                    "code": otp_data["code"],
                    "code_expiry": otp_data["code_expiry"],
                    "max_code_try": otp_data["max_code_try"],
                    "code_max_out": otp_data["code_max_out"],
                 }
                 }
            )

        if otp_data["code_max_out"] > local_time:
            return response.Response(
                {"message": "Вы много раз запросили код попробуйте через 10 мин"}
            )

        if otp_data["max_code_try"] > 0:
            otp_data["max_code_try"] = int(otp_data["max_code_try"]) - 1
            otp_data["code"] = random.randint(100000, 999999)
            otp_data["code_expiry"] = local_time + timedelta(minutes=20)
            cache.set(key=f"otp:{phone}", value=otp_data)
            # тут будем отправить смс на номер пользователя
            # send_otp(phone=serializer.validated_data['phone'], code=otp_data['code'], code_expiry=otp_data['code_expiry'])
            
            return response.Response(
                {
                    "message": "OTP успешно генерирован.",
                    "phone": phone,
                    "code": otp_data["code"],
                    "code_expiry": otp_data["code_expiry"],
                    "max_code_try": otp_data["max_code_try"],
                    "code_max_out": otp_data["code_max_out"],
                }
            )
