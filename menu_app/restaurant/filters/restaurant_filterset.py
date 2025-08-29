from django_filters import rest_framework as filters
from menu_app.restaurant.models.restaurant import Restaurant
from django.contrib.postgres.fields import ArrayField


class RestaurantFilter(filters.FilterSet):
    tags = filters.CharFilter(method="filter_tags")

    class Meta:
        model = Restaurant
        fields = ("user_id", "name", "id", "tags")
        filter_overrides = {
            ArrayField: {
                "filter_class": filters.CharFilter,
                "extra": lambda f: {"lookup_expr": "contains"},
            },
        }

    def filter_tags(self, queryset, name, value):
        # ищем рестораны, где массив tags содержит переданное значение
        return queryset.filter(tags__contains=[value])
