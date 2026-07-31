from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task
from django.utils import timezone


@login_required
def dashboard(request):

    context = {
        "employees_count": Employee.objects.count(),
        "projects_count": Project.objects.count(),
        "tasks_count": Task.objects.count(),
        "completed_tasks": Task.objects.filter(
            status=Task.Status.COMPLETED
        ).count(),

        "projects": Project.objects.all()[:5],

        "upcoming_tasks": Task.objects.filter(
            due_date__gte=timezone.now().date()
        ).order_by("due_date")[:5],
    }

    return render(
        request,
        "dashboard/index.html",
        context
    )