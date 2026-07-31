from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),


    path(
        "",
        include("apps.accounts.urls")
    ),


    path(
        "dashboard/",
        include("apps.dashboard.urls")
    ),


    path(
        "projects/",
        include("apps.projects.urls")
    ),


    path(
        "tasks/",
        include("apps.tasks.urls")
    ),


    path(
        "employees/",
        include("apps.employees.urls")
    ),

]