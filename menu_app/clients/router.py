from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from menu_app.clients.api import *


class ClientRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]

clientrouter = ClientRouter()


clientrouter.register(r'restaurants', RestaurantClientView, basename='restaurant')
clientrouter.register(r'menus', MenuClientView, basename='menu')
clientrouter.register(r'cateogrys', CategoryClientView, basename='category')