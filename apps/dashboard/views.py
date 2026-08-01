from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task

from apps.accounts.permissions import (
    is_admin,
    is_manager,
)

@login_required
def dashboard(request):

    user = request.user


    if is_admin(user):

        projects = Project.objects.all()
        employees = Employee.objects.all()
        tasks = Task.objects.all()


    elif is_manager(user):

        employee = user.employee

        projects = Project.objects.filter(
            manager=employee
        )

        employees = Employee.objects.filter(
            project_assignments__project__manager=employee
        ).distinct()

        tasks = Task.objects.filter(
            project__manager=employee
        )


    else:

        employee = user.employee

        projects = Project.objects.filter(
            assignments__employee=employee
        )

        employees = Employee.objects.filter(
            id=employee.id
        )

        tasks = Task.objects.filter(
            assigned_to=employee
        )


    context = {

        "employees_count": employees.count(),

        "projects_count": projects.count(),

        "tasks_count": tasks.count(),

        "completed_tasks": tasks.filter(
            status=Task.Status.COMPLETED
        ).count(),

        "projects": projects[:5],

        "upcoming_tasks": tasks.filter(
            due_date__gte=timezone.now().date()
        ).order_by(
            "due_date"
        )[:5],
    }


    return render(
        request,
        "dashboard/index.html",
        context
    )