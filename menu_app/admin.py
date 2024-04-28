from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "availability", "is_active","restaurant",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_per_page = 10
    list_filter = ("restaurant",)
    search_fields = ["restaurant__name","category__name"]
    actions_on_top = False
    actions_on_bottom = True


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "adress", "is_active",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_filter = ("user",)
    search_fields = ["user__username"]
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order",)
    list_display_links = ("name",)
    list_editable = ("is_active",)
    list_filter = ("restaurant",)
    search_fields = ["restaurant__name"]
    list_per_page = 20
    actions_on_top = False
    actions_on_bottom = True



admin.site.register(Menu, MenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Promo)
