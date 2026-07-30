from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "job_title",
        "department",
        "status",
        "hire_date",
        "user",
    )

    list_filter = (
        "status",
        "department",
        "hire_date",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "job_title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    date_hierarchy = "hire_date"


    @admin.display(
        description="Name"
    )
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"