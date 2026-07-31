from datetime import date

from django.test import TestCase

from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task


class TaskTests(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Smith",
            email="john@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        self.project = Project.objects.create(
            name="ERP System",
            start_date=date.today(),
        )

    def test_create_task(self):

        task = Task.objects.create(
            title="Setup database",
            project=self.project,
            assigned_to=self.employee,
        )

        self.assertEqual(
            task.project,
            self.project
        )

        self.assertEqual(
            task.assigned_to,
            self.employee
        )

        self.assertEqual(
            task.status,
            Task.Status.TODO
        )

        self.assertEqual(
            task.priority,
            Task.Priority.MEDIUM
        )

    def test_task_requires_project(self):
        task = Task(
            title="Orphan task",
            assigned_to=self.employee,
        )

        with self.assertRaises(Exception):
            task.full_clean()

    def test_deleting_project_deletes_tasks(self):

        task = Task.objects.create(
            title="Delete me",
            project=self.project,
            assigned_to=self.employee,
        )

        self.project.delete()

        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )

    def test_due_date_cannot_be_before_start_date(self):

        task = Task(
            title="Invalid dates",
            project=self.project,
            assigned_to=self.employee,
            start_date=date(2026, 7, 10),
            due_date=date(2026, 7, 5),
        )

        with self.assertRaises(Exception):
            task.full_clean()