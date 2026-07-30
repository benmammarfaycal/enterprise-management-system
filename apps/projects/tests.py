from datetime import date

from django.test import TestCase

from apps.employees.models import Employee
from apps.projects.models import Project, ProjectAssignment


class ProjectAssignmentTests(TestCase):

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

    def test_create_project_assignment(self):

        assignment = ProjectAssignment.objects.create(
            project=self.project,
            employee=self.employee,
            role=ProjectAssignment.Role.DEVELOPER,
            hours_per_week=40,
        )

        self.assertEqual(
            assignment.project,
            self.project
        )

        self.assertEqual(
            assignment.employee,
            self.employee
        )

    def test_hours_per_week_cannot_exceed_40(self):

        assignment = ProjectAssignment(
            project=self.project,
            employee=self.employee,
            role=ProjectAssignment.Role.DEVELOPER,
            hours_per_week=50,
        )

        with self.assertRaises(Exception):
            assignment.full_clean()

    def test_duplicate_assignment_is_not_allowed(self):

        ProjectAssignment.objects.create(
            project=self.project,
            employee=self.employee,
            role=ProjectAssignment.Role.DEVELOPER,
        )

        with self.assertRaises(Exception):

            ProjectAssignment.objects.create(
                project=self.project,
                employee=self.employee,
                role=ProjectAssignment.Role.TESTER,
            )

    def test_project_can_only_have_one_manager(self):
        ProjectAssignment.objects.create(
            project=self.project,
            employee=self.employee,
            role=ProjectAssignment.Role.PROJECT_MANAGER,
        )

        another_employee = Employee.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        second_assignment = ProjectAssignment(
            project=self.project,
            employee=another_employee,
            role=ProjectAssignment.Role.PROJECT_MANAGER,
        )

        with self.assertRaises(Exception):
            second_assignment.full_clean()

    def test_project_can_have_manager(self):
        manager = Employee.objects.create(
            first_name="Mike",
            last_name="Johnson",
            email="mike@test.com",
            hire_date=date.today(),
            job_title="Manager",
            department="IT",
        )

        self.project.manager = manager
        self.project.save()

        self.assertEqual(
            self.project.manager,
            manager
        )

    def test_employee_count_returns_number_of_assigned_employees(self):
        employee2 = Employee.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        ProjectAssignment.objects.create(
            project=self.project,
            employee=self.employee,
            role=ProjectAssignment.Role.DEVELOPER,
        )

        ProjectAssignment.objects.create(
            project=self.project,
            employee=employee2,
            role=ProjectAssignment.Role.TESTER,
        )

        self.assertEqual(
            self.project.employee_count,
            2
        )

    def test_manager_name_returns_full_name(self):
        manager = Employee.objects.create(
            first_name="Michael",
            last_name="Brown",
            email="michael@test.com",
            hire_date=date.today(),
            job_title="Project Manager",
            department="IT",
        )

        self.project.manager = manager
        self.project.save()

        self.assertEqual(
            self.project.manager_name,
            "Michael Brown"
        )
