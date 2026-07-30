from django.db import models
from apps.employees.models import Employee
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = "PLANNING", "Planning"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    name = models.CharField(max_length=200)
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
    )
    description = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def employee_count(self):
        return self.assignments.count()

    @property
    def manager_name(self):
        if self.manager:
            return f"{self.manager.first_name} {self.manager.last_name}"
        return "No manager assigned"


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["status"]),
        ]


class ProjectAssignment(models.Model):

    class Role(models.TextChoices):
        PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
        DEVELOPER = "DEVELOPER", "Developer"
        DESIGNER = "DESIGNER", "Designer"
        TESTER = "TESTER", "Tester"
        OTHER = "OTHER", "Other"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="project_assignments"
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.OTHER
    )

    assigned_date = models.DateField(
        auto_now_add=True
    )

    hours_per_week = models.PositiveIntegerField(
        default=40,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(40),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        if self.role == self.Role.PROJECT_MANAGER:
            exists = ProjectAssignment.objects.filter(
                project=self.project,
                role=self.Role.PROJECT_MANAGER
            ).exclude(
                id=self.id
            ).exists()

            if exists:
                raise ValidationError(
                    "A project can only have one project manager."
                )

    def __str__(self):
        return f"{self.employee} - {self.project}"

    class Meta:
        ordering = ["-assigned_date"]
        verbose_name = "Project Assignment"
        verbose_name_plural = "Project Assignments"

        constraints = [
            models.UniqueConstraint(
                fields=["project", "employee"],
                name="unique_employee_project_assignment"
            ),
        ]