from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Employee, WeekSchedule, DaySchedule
from .services import get_week_start

User = get_user_model()


class ScheduleTests(APITestCase):

    def setUp(self):
        # OWNER
        self.owner = User.objects.create_user(
            username="owner",
            password="pass",
            level="OWNER"
        )

        # обычный пользователь
        self.user = User.objects.create_user(
            username="user",
            password="pass",
            level="USER"
        )

        self.employee = Employee.objects.create(
            fio="Test Employee",
            user=self.user
        )

    # ==========================
    # WEEKLY VIEW
    # ==========================

    def test_weekly_schedule_requires_auth(self):
        response = self.client.get("/schedule/weekly/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_weekly_schedule_returns_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/schedule/weekly/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("currentWeek", response.data)
        self.assertIn("employees", response.data)

    # ==========================
    # ADD EMPLOYEE
    # ==========================

    def test_add_employee_only_owner(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/schedule/add/", {
            "fio": "New Employee",
            "username": "newuser",
            "password": "pass"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_add_employee(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post("/schedule/add/", {
            "fio": "New Employee",
            "username": "newuser",
            "password": "pass"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(fio="New Employee").exists())

    # ==========================
    # DELETE EMPLOYEE
    # ==========================

    def test_owner_can_delete_employee(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(f"/schedule/delete/{self.employee.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

    def test_user_cannot_delete_employee(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/schedule/delete/{self.employee.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==========================
    # UPDATE SCHEDULE
    # ==========================

    def test_update_schedule(self):
        self.client.force_authenticate(user=self.user)

        monday = get_week_start(date.today())

        payload = [
            {
                "employeeId": self.employee.id,
                "weekStart": str(monday),
                "schedule": {
                    "monday": {"start": "09:00", "end": "18:00"},
                    "tuesday": {"start": "", "end": ""},
                    "wednesday": {"start": "", "end": ""},
                    "thursday": {"start": "", "end": ""},
                    "friday": {"start": "", "end": ""},
                    "saturday": {"start": "", "end": ""},
                    "sunday": {"start": "", "end": ""},
                }
            }
        ]

        response = self.client.post("/schedule/update/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        week = WeekSchedule.objects.get(employee=self.employee, start_of_week=monday)
        monday_day = DaySchedule.objects.get(week=week, weekday=0)

        self.assertEqual(str(monday_day.start), "09:00:00")
        self.assertEqual(str(monday_day.end), "18:00:00")
