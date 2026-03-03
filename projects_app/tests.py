from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from schedule_app.models import Employee
from .models import Project

User = get_user_model()


class ProjectTests(APITestCase):

    def setUp(self):
        # создаём пользователя
        self.user = User.objects.create_user(
            username="user",
            password="pass",
            level="USER"
        )

        self.employee = Employee.objects.create(
            fio="Test Employee",
            user=self.user
        )

        self.project = Project.objects.create(name="Test Project")
        self.project.employees.add(self.employee)

    # ==========================
    # AUTH CHECK
    # ==========================

    def test_project_list_requires_auth(self):
        response = self.client.get("/projects/all/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==========================
    # PROJECT LIST
    # ==========================

    def test_project_list_returns_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/projects/all/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("currentWeek", response.data)
        self.assertIn("projects", response.data)
        self.assertIn("Test Project", response.data["projects"])

    # ==========================
    # PROJECT DETAIL
    # ==========================

    def test_project_detail(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/projects/{self.project.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Project")
        self.assertEqual(len(response.data["employees"]), 1)

    # ==========================
    # ADD EMPLOYEE TO PROJECT
    # ==========================

    def test_add_employee_to_project(self):
        self.client.force_authenticate(user=self.user)

        new_employee = Employee.objects.create(fio="Second Employee")

        payload = [
            {
                "action": "add",
                "project": "Test Project",
                "fio": [
                    {"id": new_employee.id, "fio": new_employee.fio}
                ]
            }
        ]

        response = self.client.post("/projects/change/", payload, format="json")

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.employees.count(), 2)

    # ==========================
    # REMOVE EMPLOYEE
    # ==========================

    def test_remove_employee_from_project(self):
        self.client.force_authenticate(user=self.user)

        payload = [
            {
                "action": "remove",
                "project": "Test Project",
                "fio": [
                    {"id": self.employee.id, "fio": self.employee.fio}
                ]
            }
        ]

        response = self.client.post("/projects/change/", payload, format="json")

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.employees.count(), 0)

    # ==========================
    # INVALID PAYLOAD
    # ==========================

    def test_invalid_payload_returns_400(self):
        self.client.force_authenticate(user=self.user)

        payload = [
            {
                "wrong": "data"
            }
        ]

        response = self.client.post("/projects/change/", payload, format="json")

        self.assertEqual(response.status_code, 400)
