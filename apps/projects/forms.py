from django import forms
from .models import Project
from apps.employees.models import Employee
from .models import ProjectAssignment

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "description",
            "manager",
            "start_date",
            "end_date",
            "budget",
            "status",
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }


    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)


        if user and user.role == user.Role.MANAGER:

            self.fields.pop("manager")

class ProjectAssignmentForm(forms.ModelForm):

    class Meta:

        model = ProjectAssignment

        fields = [
            "employee",
            "role",
            "hours_per_week",
        ]