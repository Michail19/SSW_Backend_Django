from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from schedule_app.models import Employee, DaySchedule, WeekSchedule, CurrentWeek
from projects_app.models import Project
from datetime import date, time
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Seeding database...")

        # Очистка
        WeekSchedule.objects.all().delete()
        DaySchedule.objects.all().delete()
        Employee.objects.all().delete()
        Project.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        CurrentWeek.objects.all().delete()

        # Current week
        CurrentWeek.objects.create(
            week_range="02-08 june 2025"
        )

        # Пользователи + сотрудники
        employees_data = [
            ("ershov.m", "Ершов Михаил Алексеевич", "OWNER"),
            ("ivanov.i", "Иванов Иван Иванович", "OWNER"),
            ("petrov.p1", "Петров Петр Петрович", "USER"),
            ("petrov.p2", "Петров Петр Сергеевич", "USER"),
            ("sidorov.s", "Сидоров Сергей Васильевич", "USER"),
            ("kuznetsova.n", "Кузнецова Надежда Игоревна", "USER"),
            ("smirnov.v", "Смирнов Виктор Петрович", "USER"),
            ("alekseeva.l", "Алексеева Людмила Павловна", "USER"),
            ("fedorov.d", "Фёдоров Дмитрий Аркадьевич", "USER"),
            ("egorova.e", "Егорова Екатерина Владимировна", "USER"),
            ("nikitin.a", "Никитин Алексей Валерьевич", "USER"),
            ("tarasova.m", "Тарасова Мария Олеговна", "USER"),
        ]

        employees = []

        for username, fio, level in employees_data:
            user = User.objects.create_user(
                username=username,
                password="1234",   # тестовый пароль
                level=level
            )
            emp = Employee.objects.create(
                fio=fio,
                user=user
            )
            employees.append(emp)

        # Проекты
        project_names = [
            "Project_Yandex_ONO-TEBE-NADO",
            "Project_Yandex_BLOG",
            "Project_Yandex_WEB-LAREK",
            "Project_Yandex_MESTO-PROJECT",
            "Project_Yandex_TRAVEL",
            "Project_Yandex_UCHEBA",
        ]

        projects = []
        for name in project_names:
            projects.append(Project.objects.create(project_name=name))

        # Связи сотрудников и проектов
        for emp in employees[:3]:  # первые 3 во всех проектах
            emp.project_set.set(projects)

        # Создание расписаний
        def create_day(start, end):
            return DaySchedule.objects.create(
                start=start,
                end=end
            )

        # Пример: сотрудник 1
        week_start = date(2025, 10, 20)

        mon = create_day(time(8, 0), time(13, 40))
        tue = create_day(time(8, 0), time(15, 30))
        wed = create_day(time(15, 20), time(20, 0))
        thu = create_day(time(15, 20), time(20, 0))
        fri = create_day(time(8, 0), time(15, 30))
        sat = create_day(None, None)
        sun = create_day(None, None)

        WeekSchedule.objects.create(
            employee=employees[0],
            start_of_week=week_start,
            monday=mon,
            tuesday=tue,
            wednesday=wed,
            thursday=thu,
            friday=fri,
            saturday=sat,
            sunday=sun,
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
