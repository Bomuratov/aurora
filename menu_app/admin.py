from django.contrib import admin
from .models import *
# from users.models import AppUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# from users.forms import CustomUserChangeForm, CustomUserCreationForm


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "description")
    list_display_links = ("name",)
    list_editable = ("price", "category", "description")
    list_per_page = 10
    list_filter = ("restaurant",)
    actions_on_top = False
    actions_on_bottom = True


class TableAdmin(admin.ModelAdmin):
    list_display = ("type", "number", "restaurant", "adress_table", "percent")


# class UserAdmin(admin.ModelAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = AppUser
#     list_display = (
#         "email",
#         # "get_first_name",
#         # "get_last_name",
#         "is_active",
#         "is_staff",
#         "is_superuser",
#     )
#     search_fields = ("email",)
#     ordering = ("email",)

    # def get_first_name(self, obj):
    #     return obj.first_name

    # def get_last_name(self, obj):
    #     return obj.last_name

    # get_first_name.short_description = "First Name"
    # get_last_name.short_description = "Last Name"


# admin.site.register(AppUser, UserAdmin)
admin.site.register(Menu, MenuAdmin)
# admin.site.register(Table, TableAdmin)
admin.site.register(Restaurant)
# admin.site.register(Adress_table)
admin.site.register(Category)
