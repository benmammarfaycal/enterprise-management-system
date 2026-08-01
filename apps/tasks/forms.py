from django import forms
from .models import Task
from apps.accounts.permissions import is_manager


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "project",
            "assigned_to",
            "start_date",
            "due_date",
            "status",
            "priority",
        ]


    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        if user and is_manager(user):

            self.fields["project"].queryset = (
                user.employee.managed_projects.all()
            )