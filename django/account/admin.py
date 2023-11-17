from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


# Unregister default ModelAdmins
admin.site.unregister(Group)


class UserAdmin(UserAdmin):
    """
    Customise the admin interface: User
    """

    model = User
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'date_joined', 'last_login']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['role', 'is_active']
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'password',
                    'is_active',
                    'date_joined',
                    'last_login'
                ),
            },
        ),
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Register
admin.site.register(User, UserAdmin)
