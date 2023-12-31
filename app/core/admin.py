"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the admin page"""
    ordering = ['id']
    list_display = ['email', 'name', 'role']
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Picture)
