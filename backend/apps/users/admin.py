from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_email_verified",
        "is_staff",
        "is_active",
    )

    list_display_links = (
        "email",
        "id",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_email_verified",
    )

    ordering = ("email",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                )
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "is_email_verified",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",

                ),
            },
        ),
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )