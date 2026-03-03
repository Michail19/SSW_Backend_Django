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
    week, created = WeekSchedule.objects.get_or_create(
        employee=employee,
        start_of_week=monday
    )

    if created:
        for i in range(7):
            DaySchedule.objects.create(
                week=week,
                weekday=i
            )

    return week


def create_empty_week(employee, week_start):
    # Сначала создаём объект недели
    week_obj = WeekSchedule.objects.create(
        employee=employee,
        start_of_week=week_start
    )

    # Создаём дни для недели
    days = {}
    for i, day_name in enumerate(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
        day = DaySchedule.objects.create(
            week=week_obj,
            weekday=i  # 0=Monday ... 6=Sunday
        )
        days[day_name] = day

    return days
