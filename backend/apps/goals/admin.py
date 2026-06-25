from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "organization",
        "department",
        "status",
        "priority",
        "due_date",
    )

    list_filter = (
        "status",
        "priority",
        "organization",
    )

    search_fields = (
        "title",
    )