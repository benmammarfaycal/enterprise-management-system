from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def project_list(request):

    projects = Project.objects.all()

    context = {
        "projects": projects
    }

    return render(
        request,
        "projects/project_list.html",
        context
    )