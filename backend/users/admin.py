from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    readonly_fields = ['date_joined']
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('username',)
    list_filter = ('email', 'username',)
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'username',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'username',
                    'password'
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
