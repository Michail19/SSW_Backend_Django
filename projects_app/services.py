from datetime import date, timedelta
from calendar import month_name
from schedule_app.models import Employee
from .models import Project
from django.db import transaction


def format_current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    start_day = monday.strftime("%d")
    end_day = sunday.strftime("%d")
    month = month_name[monday.month].lower()
    year = monday.year

    return f"{start_day}-{end_day} {month} {year}"


def get_project_by_id(project_id):
    project = Project.objects.prefetch_related("employees").get(id=project_id)
    return project


def get_full_projects():
    projects = Project.objects.prefetch_related("employees").all()

    projects_map = {}

    for project in projects:
        employees = [
            {"id": emp.id, "fio": emp.fio}
            for emp in project.employees.all()
        ]
        projects_map[project.name] = employees

    return {
        "currentWeek": format_current_week(),
        "projects": projects_map
    }


@transaction.atomic
def change_employee(request_list):
    for dto in request_list:
        project_name = dto["project"]
        action = dto["action"]
        employees_data = dto["fio"]

        project, _ = Project.objects.get_or_create(name=project_name)

        for emp_data in employees_data:
            employee = Employee.objects.get(id=emp_data["id"])

            if action.lower() == "add":
                project.employees.add(employee)

            elif action.lower() == "remove":
                project.employees.remove(employee)
