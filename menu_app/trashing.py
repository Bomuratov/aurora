# # Ресторан по имени
# class Restaurant_view(ModelViewSet):
#     queryset = Restaurant.objects.all()
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = RestaurantSerializers
#     lookup_field = "name"


# # Категории фильтрация по ресторанам
# class Category_view(ModelViewSet):
#     queryset = Category.objects.all()
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     serializer_class = CategorySerializer
#     # permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         restaurant_name = self.kwargs["name_restaurant"]
#         restaurant = get_object_or_404(Restaurant, name=restaurant_name)
#         return Category.objects.filter(restaurant=restaurant)


# # Меню фильтрация по ресторанам
# class Menu_view(ModelViewSet):
#     queryset = Menu.objects.all()
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     serializer_class = MenuSerializer
#     # permission_classes = (IsAuthenticated,)


#     def get_queryset(self):
#         restaurant_name = self.kwargs["name_restaurant"]
#         restaurant = get_object_or_404(Restaurant, name=restaurant_name)
#         return Menu.objects.filter(restaurant=restaurant)


# class Menu_Update_Delete_View(ModelViewSet):
#     queryset = Menu.objects.all()
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     serializer_class = MenuSerializer
#     lookup_field = "pk"





# urlpatterns = [
#     # path("api/", include(router.urls)),
#     # path(
#     #     "api/restaurant/<str:name>/",
#     #     Restaurant_view.as_view({"get": "retrieve"}),
#     #     name="table",
#     # ),
#     # # path(
#     # #     "api/table/<str:name_restaurant>/",
#     # #     Table_view.as_view({"get": "list"}),
#     # #     name="table",
#     # # ),
#     # path(
#     #     "api/menu/<str:name_restaurant>/",
#     #     Menu_view.as_view({"get": "list"}),
#     #     name="menu",
#     # ),
#     # path("api/menu/", Menu_view.as_view({"post": "create"}), name="menu"),
#     # path(
#     #     "api/category_get/<str:name_restaurant>/",
#     #     Category_view.as_view({"get": "list"}),
#     #     name="category",
#     # ),
#     # path(
#     #     "api/menu/<int:pk>/update",
#     #     Menu_Update_Delete_View.as_view({"put": "update"}),
#     #     name="menu_update",
#     # ),
#     # path(
#     #     "api/menu/<int:pk>/delete",
#     #     Menu_Update_Delete_View.as_view({"delete": "destroy"}),
#     #     name="menu",
#     # ),
#     # path(
#     #     "api/category_post/",
#     #     Category_view.as_view({"post": "create"}),
#     #     name="category",
#     # ),
# ]