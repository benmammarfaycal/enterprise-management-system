from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "project",
        "assigned_to",
        "status",
        "priority",
        "due_date",
    )

    list_filter = (
        "status",
        "priority",
        "project",
    )

    search_fields = (
        "title",
        "description",
        "project__name",
        "assigned_to__first_name",
        "assigned_to__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "due_date",
    )