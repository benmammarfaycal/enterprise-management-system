from django.test import TestCase
from apps.accounts.models import User
from .models import Employee
from datetime import date


class EmployeeModelTest(TestCase):

    def test_create_employee_without_user(self):
        employee = Employee.objects.create(
            first_name="John",
            last_name="Smith",
            email="john.smith@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        self.assertEqual(employee.first_name, "John")
        self.assertIsNone(employee.user)


    def test_employee_can_be_linked_to_user(self):
        user = User.objects.create_user(
            email="john@test.com",
            password="password123",
            first_name="John",
            last_name="Smith",
        )

        employee = Employee.objects.create(
            user=user,
            first_name="John",
            last_name="Smith",
            email="employee@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        self.assertEqual(employee.user, user)


    def test_employee_string_representation(self):
        employee = Employee.objects.create(
            first_name="John",
            last_name="Smith",
            email="john2@test.com",
            hire_date=date.today(),
            job_title="Developer",
            department="IT",
        )

        self.assertEqual(
            str(employee),
            "John Smith (Developer)"
        )