from django.contrib import admin
from .models import User, UserRole, Permissions, UserSettings
from .models import User, UserLocation




class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "is_user",  "is_vendor", "is_active")
    list_display_links = ("first_name",)
    list_editable = ("is_active", "is_user",  "is_vendor",)
    list_per_page = 30
    actions_on_top = False
    actions_on_bottom = True


class LocationAdmin(admin.ModelAdmin):
    list_display = ("user","address", "is_active",)
    list_editable = ("is_active",)
    list_filter = ("user",)

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "permissions")


admin.site.register(User, UserAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserSettings)
admin.site.register(Permissions)
admin.site.register(UserLocation, LocationAdmin)

