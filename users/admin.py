from django.contrib import admin
from .models import User, UserRole, Permissions



class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "is_user",  "is_vendor", "is_active")
    list_display_links = ("first_name",)
    list_editable = ("is_active", "is_user",  "is_vendor",)
    list_per_page = 30
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(User, UserAdmin)
admin.site.register(UserRole)
admin.site.register(Permissions)