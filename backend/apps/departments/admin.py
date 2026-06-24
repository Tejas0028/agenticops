from django.contrib import admin

from .models import Department, DepartmentMembership


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "is_active",
        "created_at",
    )

    list_filter = (
        "organization",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "department",
        "organization_membership",
        "role",
    )

    search_fields = (
        "organization_membership__user__username",
    )