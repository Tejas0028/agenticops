from django.contrib import admin

from .models import Organization,Membership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    search_fields = ("name",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "organization",
        "role",
    )

    list_display_links = (
        "id",
        "user",
    )