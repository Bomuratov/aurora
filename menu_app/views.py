from .viewset import *
from .serializers import *
from .models import *


class RestaurantView(CustomViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer



class CategoryView(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.get_filtered_queryset(Category, "restaurant", "restaurant_name")
    



class MenuView(CustomViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


    def get_queryset(self):
        return self.get_filtered_queryset(Menu, "restaurant", "restaurant_name")