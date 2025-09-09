from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""

    # Add azure_oid to the fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Azure AD Integration", {"fields": ("azure_oid",)}),
    )

    # Add azure_oid to list display
    list_display = BaseUserAdmin.list_display + ("azure_oid",)

    # Add search by azure_oid
    search_fields = BaseUserAdmin.search_fields + ("azure_oid",)

    # Make azure_oid readonly in admin
    readonly_fields = ("azure_oid",)
