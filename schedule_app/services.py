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

    # Создаём неделю для каждого сотрудника
    for e in employees:
        get_or_create_week(e, monday)

    return monday, employees


def get_or_create_week(employee, monday):
    week, created = WeekSchedule.objects.get_or_create(
        employee=employee,
        start_of_week=monday
    )

    if created:
        days = {}
        for day_name in [
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"
        ]:
            day = DaySchedule.objects.create()
            days[day_name] = day

        for key, value in days.items():
            setattr(week, key, value)

        week.save()

    return week
