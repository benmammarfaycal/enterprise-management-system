from django.contrib.auth.decorators import login_required
from .models import Project
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from apps.accounts.permissions import (
    is_admin,
    is_manager
)
from .forms import ProjectAssignmentForm
from .forms import ProjectForm
from django.shortcuts import render, redirect

@login_required
def project_list(request):

    user = request.user

    if is_admin(user):

        projects = Project.objects.all()


    elif is_manager(user):

        employee = user.employee

        projects = Project.objects.filter(
            manager=employee
        )


    else:

        employee = user.employee

        projects = Project.objects.filter(
            assignments__employee=employee
        )


    context = {
        "projects": projects
    }


    return render(
        request,
        "projects/project_list.html",
        context
    )

@login_required
def project_detail(request, pk):

    project = get_object_or_404(
        Project,
        id=pk
    )


    if not user_can_access_project(
        request.user,
        project
    ):
        raise PermissionDenied


    context = {
        "project": project
    }


    return render(
        request,
        "projects/project_detail.html",
        context
    )

@login_required
def project_update(request, pk):

    if not is_admin(request.user):
        raise PermissionDenied

    project = get_object_or_404(
        Project,
        id=pk
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect(
                "projects:detail",
                pk=project.id
            )

    else:

        form = ProjectForm(
            instance=project
        )

    context = {
        "form": form,
        "project": project,
    }

    return render(
        request,
        "projects/project_form.html",
        context
    )

def user_can_access_project(user, project):

    if is_admin(user):
        return True


    if is_manager(user):

        return project.manager == user.employee


    return project.assignments.filter(
        employee=user.employee
    ).exists()

@login_required
def project_create(request):

    if not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("projects:list")

    else:
        form = ProjectForm()

    context = {
        "form": form
    }

    return render(
        request,
        "projects/project_form.html",
        context
    )


@login_required
def project_delete(request, pk):

    if not is_admin(request.user):
        raise PermissionDenied


    project = get_object_or_404(
        Project,
        id=pk
    )


    if request.method == "POST":

        project.delete()

        return redirect(
            "projects:list"
        )


    context = {
        "project": project
    }


    return render(
        request,
        "projects/project_confirm_delete.html",
        context
    )

@login_required
def assign_employee(request, pk):

    project = get_object_or_404(
        Project,
        id=pk
    )


    if is_admin(request.user):

        pass


    elif is_manager(request.user):

        if project.manager != request.user.employee:
            raise PermissionDenied


    else:

        raise PermissionDenied



    if request.method == "POST":

        form = ProjectAssignmentForm(
            request.POST
        )

        if form.is_valid():

            assignment = form.save(
                commit=False
            )

            assignment.project = project

            assignment.save()


            return redirect(
                "projects:detail",
                pk=project.id
            )


    else:

        form = ProjectAssignmentForm()



    context = {

        "form": form,

        "project": project,

    }


    return render(
        request,
        "projects/project_assign.html",
        context
    )