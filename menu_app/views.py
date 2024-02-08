from .viewset import *
from .serializers import *
from .models import *
from menu_app.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class RestaurantView(CustomViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer



class CategoryView(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.get_filtered_queryset(Category, "restaurant", "restaurant_name")
    
    @action(detail=False, methods=['post'], url_path='update_order')
    def post_update(self, request):
        category_ids = request.data 
        for index, category_id in enumerate(category_ids):
            category = Category.objects.get(id=category_id)
            category.order = index 
            category.save()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)



class MenuView(CustomViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


    def get_queryset(self):
        return self.get_filtered_queryset(Menu, "restaurant", "restaurant_name")
    

class CustomTokenObtain(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer