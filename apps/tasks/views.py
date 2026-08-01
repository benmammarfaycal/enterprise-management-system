from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Task
from .forms import TaskForm

from apps.accounts.permissions import (
    is_admin,
    is_manager
)


def user_can_access_task(user, task):

    if is_admin(user):
        return True


    if is_manager(user):
        return task.project.manager == user.employee


    return task.assigned_to == user.employee



@login_required
def task_list(request):

    user = request.user


    if is_admin(user):

        tasks = Task.objects.all()


    elif is_manager(user):

        tasks = Task.objects.filter(
            project__manager=user.employee
        )


    else:

        tasks = Task.objects.filter(
            assigned_to=user.employee
        )


    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks
        }
    )



@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        id=pk
    )


    if not user_can_access_task(
        request.user,
        task
    ):
        raise PermissionDenied


    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task
        }
    )



@login_required
def task_create(request):

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            user=request.user
        )


        if form.is_valid():

            task = form.save()

            return redirect(
                "tasks:detail",
                task.id
            )


    else:

        form = TaskForm(
            user=request.user
        )


    return render(
        request,
        "tasks/task_form.html",
        {
            "form":form
        }
    )



@login_required
def task_update(request, pk):

    task = get_object_or_404(
        Task,
        id=pk
    )


    if not is_admin(request.user) and not is_manager(request.user):
        raise PermissionDenied


    if not user_can_access_task(
        request.user,
        task
    ):
        raise PermissionDenied



    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task,
            user=request.user
        )


        if form.is_valid():

            form.save()

            return redirect(
                "tasks:detail",
                task.id
            )


    else:

        form = TaskForm(
            instance=task,
            user=request.user
        )


    return render(
        request,
        "tasks/task_form.html",
        {
            "form":form
        }
    )



@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        id=pk
    )


    if not user_can_access_task(
        request.user,
        task
    ):
        raise PermissionDenied



    if request.method == "POST":

        task.delete()

        return redirect(
            "tasks:list"
        )


    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task":task
        }
    )

@login_required
def task_update_status(request, pk):

    task = get_object_or_404(
        Task,
        id=pk
    )


    # L'employé ne peut modifier que ses propres tâches
    if task.assigned_to != request.user.employee:

        raise PermissionDenied


    if request.method == "POST":

        status = request.POST.get("status")

        if status in dict(Task.Status.choices):

            task.status = status
            task.save()


        return redirect(
            "tasks:detail",
            pk=task.id
        )


    return redirect(
        "tasks:detail",
        pk=task.id
    )