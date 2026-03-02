from datetime import timedelta
from django.utils.timezone import now
from .models import Employee, WeekSchedule, DaySchedule

def get_week_start(date):
    return date - timedelta(days=date.weekday())


def get_full_schedule_for_week(request_user, date=None):
    if date is None:
        date = now().date()

    monday = get_week_start(date)

    employees = Employee.objects.all()

    # Сортируем: текущий пользователь первый
    if hasattr(request_user, "employee"):
        current = request_user.employee
        employees = sorted(
            employees,
            key=lambda e: 0 if e.id == current.id else 1
        )

    # Создаем недели для каждого сотрудника
    for e in employees:
        get_or_create_week(e, monday)

    return monday, employees


def get_or_create_week(employee, monday):
    week = WeekSchedule.objects.filter(employee=employee, start_of_week=monday).first()
    if week:
        return week

    # Создаем дни
    days = {}
    for day_name in [
        "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]:
        days[day_name] = DaySchedule.objects.create()

    # Создаем неделю с привязкой ко всем дням
    week = WeekSchedule.objects.create(
        employee=employee,
        start_of_week=monday,
        monday=days["monday"],
        tuesday=days["tuesday"],
        wednesday=days["wednesday"],
        thursday=days["thursday"],
        friday=days["friday"],
        saturday=days["saturday"],
        sunday=days["sunday"]
    )

    return week

def create_empty_week(employee, week_start):
    return {
        "monday": DaySchedule.objects.create(),
        "tuesday": DaySchedule.objects.create(),
        "wednesday": DaySchedule.objects.create(),
        "thursday": DaySchedule.objects.create(),
        "friday": DaySchedule.objects.create(),
        "saturday": DaySchedule.objects.create(),
        "sunday": DaySchedule.objects.create(),
    }
