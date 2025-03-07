# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from menu_app.models import Restaurant


# class UserTokenSerializer(TokenObtainPairSerializer):
    
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         restaurant = ', '.join(Restaurant.objects.filter(user_id=user.id).values_list('name', flat=True))
#         token['email'] = user.email
#         token['is_user'] = user.is_user
#         token['is_vendor'] = user.is_vendor
#         token["vendor"] = restaurant if restaurant else None
#         return token