from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from menu_app.restaurant.models import Restaurant, RestaurantDetails


class OptionsAdmin(admin.ModelAdmin):
    list_display = ("id", "menu",)

class VariantsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "option_group_id",)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "open_time", "close_time", "restaurant")


class MenuAdmin(admin.ModelAdmin):
    list_display = ("id","name", "category", "availability", "is_active","restaurant",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_per_page = 10
    list_filter = ("restaurant",)
    search_fields = ["restaurant__name","category__name"]
    actions_on_top = False
    actions_on_bottom = True


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "is_active",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_filter = ("user",)
    search_fields = ["user__username"]
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True



class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name", "is_active", "order",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_filter = ("restaurant",)
    search_fields = ["restaurant__name"]
    list_per_page = 20
    actions_on_top = False
    actions_on_bottom = True




class DeliveryRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'restaurant',
        "name",
        'calculation_type',
        'is_active',
        'min_distance',
        'max_distance',
        'fixed_price',
        'price_per_km',
        'max_order_price_for_free_delivery',
        "price_per_percent",
        'created',
    )
    list_filter = ('calculation_type', 'is_active', 'restaurant')
    search_fields = ('restaurant__name',)
    ordering = ('restaurant', 'min_distance')
    list_editable = ('is_active',)

    fieldsets = (
        (None, {
            'fields': ('restaurant', 'calculation_type', 'is_active', "name", "description")
        }),
        ('Диапазон расстояния', {
            'fields': ('min_distance', 'max_distance')
        }),
        ('Цены', {
            'fields': ('fixed_price', 'price_per_km', "price_per_percent"),
        }),
        ('Бесплатная доставка', {
            'fields': ('max_order_price_for_free_delivery', "reverse_calculate")
        }),

    )



admin.site.register(DeliveryRule, DeliveryRuleAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(OptionGroup, OptionsAdmin)
admin.site.register(Variant, VariantsAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Promo)
admin.site.register(RestaurantDetails)
admin.site.register(Schedule, ScheduleAdmin)
