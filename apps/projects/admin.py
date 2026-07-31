from django.contrib import admin
from .models import Project, ProjectAssignment
from apps.tasks.models import Task

class ProjectAssignmentInline(admin.TabularInline):
    model = ProjectAssignment
    extra = 1

    fields = (
        "employee",
        "role",
        "hours_per_week",
        "assigned_date",
    )

    readonly_fields = (
        "assigned_date",
    )

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = (
        "title",
        "assigned_to",
        "status",
        "priority",
        "due_date",
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "manager",
    )

    list_display = (
        "id",
        "name",
        "status",
        "manager",
        "start_date",
        "end_date",
        "budget",
        "employee_count",
    )

    list_filter = (
        "status",
        "manager",
        "start_date",
    )
    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ProjectAssignmentInline,
        TaskInline,
    ]

    ordering = (
        "name",
    )


    def employee_count(self, obj):
        return len(obj.assignments.all())

    employee_count.short_description = "Employees"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            "assignments"
        )


@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "project",
        "role",
        "hours_per_week",
        "assigned_date",
    )

    list_filter = (
        "role",
        "assigned_date",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "project__name",
    )
    autocomplete_fields = (
        "employee",
        "project",
    )

