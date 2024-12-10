from rest_framework.routers import Route, DynamicRoute, SimpleRouter

from menu_app.admins.api import *


class AdminRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'post': 'create',
                     "get":"list"},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve',
                     'put': 'update',
                     'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]


adminrouter = AdminRouter()
adminrouter.register(r'restaurants', RestaurantAdminView, basename='restaurant')
adminrouter.register(r'categorys', CategoryAdminView, basename='category')
adminrouter.register(r'menus', MenuAdminView, basename='menu')
adminrouter.register(r'promos', PromoAdminView, basename='promo')

