from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from schedule_app.models import Employee, DaySchedule, WeekSchedule, CurrentWeek
from projects_app.models import Project, EmployeeProject
from datetime import date, time
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Очистка
        self.clean_database()

        # Текущая неделя
        current_week = CurrentWeek.objects.create(
            week_range="02-08 june 2025"
        )
        self.stdout.write(f"Created current week: {current_week}")

        # Создание пользователей и сотрудников
        employees = self.create_users_and_employees()
        self.stdout.write(f"Created {len(employees)} employees")

        # Создание проектов
        projects = self.create_projects()
        self.stdout.write(f"Created {len(projects)} projects")

        # Связи сотрудников с проектами
        self.create_employee_project_relations(employees, projects)

        # Создание расписаний
        self.create_schedules(employees)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))

    def clean_database(self):
        """Очистка всех таблиц"""
        WeekSchedule.objects.all().delete()
        DaySchedule.objects.all().delete()
        EmployeeProject.objects.all().delete()
        Employee.objects.all().delete()
        Project.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        CurrentWeek.objects.all().delete()
        self.stdout.write("Database cleaned")

    def create_users_and_employees(self):
        """Создание пользователей и сотрудников"""
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

        # Пароли из SQL (закодированные)
        passwords = [
            'bcrypt$$2a$12$rtfd779so3luDus8hIQ9KOOO4q8ESh9gbSlXRJvu.tBUpVihLkxua',
            'bcrypt$$2a$12$vbXQR/TY1Iu0y9JmQ9j/x.5WSx6D135JcuqWWrBMa4JjuuFDrOyQ2',
            'bcrypt$$2a$12$vUXOdJxV2gB3VO3WFOVv5OuZuZBC8sCcB71oo9aqlEzcCSbdnYHK6',
            'bcrypt$$2a$12$.Sxw9xNkktYdwetdmcrNpuxvPMembipPeh5pff8v6eFfqtVngMymW',
            'bcrypt$$2a$12$tBVDJNdxGz/gX4m1dfOMbeGnEx9ASBAUCTVf0roSUECuGxNWej/ri',
            'bcrypt$$2a$12$M6WANscAzLUmwq7cnn5VgO6DSxiVITf8N7FFe/6DCUAXKbc76kRWe',
            'bcrypt$$2a$12$woXGI0ik.Dt3vqLecLlppeHKf1UdLn5VUoRTLhMNv8iUmYHksSd7K',
            'bcrypt$$2a$12$ZqSazra/MY1.8w8bvC1XXu6JWFu3oeombl671IFC66KZBo0TFNIDm',
            'bcrypt$$2a$12$75EO/y5zBhuuEs8DCa/RSuQZmc4dSvY9jwqFZuZoWfKij7aWLQqta',
            'bcrypt$$2a$12$0wPn5oi7ZFdADgDTFC2Qn.fy5d2WI6R46SPF0kiLJ3v7sZ4r/2L/i',
            'bcrypt$$2a$12$RANZthfe/H/gDUopUuqmaudjyti94KWdSfCBhFx9h3z6P7grnwp/2',
            'bcrypt$$2a$12$4pXOcZgN37VSkq9mKqfZJO/L7AK1clPgfeCaJees4aOVNNoODejsm',
        ]

        for i, (username, fio, level) in enumerate(employees_data):
            # Проверяем, существует ли уже пользователь
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': passwords[i],  # Используем закодированный пароль из SQL
                    'level': level
                }
            )

            if not created:
                user.level = level
                user.password = passwords[i]
                user.save()

            emp, _ = Employee.objects.get_or_create(
                user=user,
                defaults={'fio': fio}
            )
            employees.append(emp)

        return employees

    def create_projects(self):
        """Создание проектов"""
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
            project, _ = Project.objects.get_or_create(project_name=name)
            projects.append(project)

        return projects

    def create_employee_project_relations(self, employees, projects):
        """Создание связей между сотрудниками и проектами"""

        # Связи из SQL data.sql
        relations = [
            # employee_id, project_indices (0-based)
            (1, [0, 1, 2, 3, 4, 5]),  # сотрудник 1 во всех проектах
            (2, [0, 1, 2, 3, 4, 5]),  # сотрудник 2 во всех проектах
            (3, [0, 1, 2, 3, 4, 5]),  # сотрудник 3 во всех проектах
            (4, [0, 5]),  # сотрудник 4: ONO-TEBE-NADO и UCHEBA
            (5, [3, 5]),  # сотрудник 5: MESTO-PROJECT и UCHEBA
            (6, [0, 1, 2]),  # сотрудник 6: ONO-TEBE-NADO, BLOG, WEB-LAREK
            (7, [5]),  # сотрудник 7: UCHEBA
            (8, [3]),  # сотрудник 8: MESTO-PROJECT
            (9, [4, 5]),  # сотрудник 9: TRAVEL, UCHEBA
            (10, [0, 1, 2]),  # сотрудник 10: ONO-TEBE-NADO, BLOG, WEB-LAREK
            (11, [0, 5]),  # сотрудник 11: ONO-TEBE-NADO, UCHEBA
            (12, [1, 2, 4, 5]),  # сотрудник 12: BLOG, WEB-LAREK, TRAVEL, UCHEBA
        ]

        for emp_idx, proj_indices in relations:
            employee = employees[emp_idx - 1]  # -1 потому что индексы с 1 в SQL
            for proj_idx in proj_indices:
                employee.projects.add(projects[proj_idx])

    def create_schedules(self, employees):
        """Создание расписаний для сотрудников"""

        # Базовая дата начала недели
        week_start = date(2025, 10, 20)

        # Расписание для сотрудника 1
        self.create_employee1_schedule(employees[0], week_start)

        # Расписание для сотрудника 2
        self.create_employee2_schedule(employees[1], week_start)

        # Расписание для сотрудников 3-8 (одинаковое)
        schedule_3_8 = self.create_standard_schedule(week_start)
        for i in range(2, 8):  # индексы 2-7 (сотрудники 3-8)
            self.assign_schedule_to_employee(employees[i], week_start, schedule_3_8)

        # Расписание для сотрудника 9
        self.create_employee9_schedule(employees[8], week_start)

        # Расписание для сотрудника 10
        self.create_employee10_schedule(employees[9], week_start)

        # Расписание для сотрудника 11
        self.create_employee11_schedule(employees[10], week_start)

        # Расписание для сотрудника 12
        self.create_employee12_schedule(employees[11], week_start)

    def create_day(self, start_time=None, end_time=None):
        """Вспомогательная функция для создания DaySchedule"""
        return DaySchedule.objects.create(start=start_time, end=end_time)

    def create_employee1_schedule(self, employee, week_start):
        """Расписание для сотрудника 1"""
        mon = self.create_day(time(8, 0), time(13, 40))
        tue = self.create_day(time(8, 0), time(15, 30))
        wed = self.create_day(time(15, 20), time(20, 0))
        thu = self.create_day(time(15, 20), time(20, 0))
        fri = self.create_day(time(8, 0), time(15, 30))
        sat = self.create_day(None, None)
        sun = self.create_day(None, None)

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=mon,
            tuesday=tue,
            wednesday=wed,
            thursday=thu,
            friday=fri,
            saturday=sat,
            sunday=sun,
        )

    def create_employee2_schedule(self, employee, week_start):
        """Расписание для сотрудника 2"""
        # Пн-Чт: 08:00-17:00
        mon_thu = self.create_day(time(8, 0), time(17, 0))
        # Пт: 08:00-16:00
        fri = self.create_day(time(8, 0), time(16, 0))
        # Сб-Вс: 10:00-14:00
        weekend = self.create_day(time(10, 0), time(14, 0))

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=mon_thu,
            tuesday=mon_thu,
            wednesday=mon_thu,
            thursday=mon_thu,
            friday=fri,
            saturday=weekend,
            sunday=weekend,
        )

    def create_standard_schedule(self, week_start):
        """Стандартное расписание для сотрудников 3-8"""
        # Пн-Пт: 09:00-18:00
        workday = self.create_day(time(9, 0), time(18, 0))
        # Сб-Вс: 10:00-15:00
        weekend = self.create_day(time(10, 0), time(15, 0))

        return {
            'monday': workday,
            'tuesday': workday,
            'wednesday': workday,
            'thursday': workday,
            'friday': workday,
            'saturday': weekend,
            'sunday': weekend,
        }

    def create_employee9_schedule(self, employee, week_start):
        """Расписание для сотрудника 9"""
        mon_wed_fri = self.create_day(time(9, 0), time(18, 0))
        thu = self.create_day(time(12, 0), time(18, 0))
        weekend = self.create_day(time(10, 0), time(15, 0))

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=mon_wed_fri,
            tuesday=mon_wed_fri,
            wednesday=mon_wed_fri,
            thursday=thu,
            friday=mon_wed_fri,
            saturday=weekend,
            sunday=weekend,
        )

    def create_employee10_schedule(self, employee, week_start):
        """Расписание для сотрудника 10"""
        mon_tue_thu = self.create_day(time(9, 0), time(18, 0))
        wed = self.create_day(time(9, 50), time(18, 10))
        fri = self.create_day(time(19, 0), time(22, 0))
        sat = self.create_day(time(11, 0), time(12, 0))
        sun = self.create_day(time(10, 0), time(15, 0))

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=mon_tue_thu,
            tuesday=mon_tue_thu,
            wednesday=wed,
            thursday=mon_tue_thu,
            friday=fri,
            saturday=sat,
            sunday=sun,
        )

    def create_employee11_schedule(self, employee, week_start):
        """Расписание для сотрудника 11"""
        mon_wed = self.create_day(time(9, 0), time(18, 0))
        tue = self.create_day(time(9, 10), time(18, 0))
        thu = self.create_day(time(9, 0), time(11, 0))
        fri = self.create_day(time(9, 30), time(18, 0))
        weekend = self.create_day(time(10, 0), time(15, 0))

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=mon_wed,
            tuesday=tue,
            wednesday=mon_wed,
            thursday=thu,
            friday=fri,
            saturday=weekend,
            sunday=weekend,
        )

    def create_employee12_schedule(self, employee, week_start):
        """Расписание для сотрудника 12"""
        # Пн-Пт: 09:00-18:00
        workday = self.create_day(time(9, 0), time(18, 0))
        # Сб: 10:00-15:00
        sat = self.create_day(time(10, 0), time(15, 0))
        # Вс: 10:00-13:00
        sun = self.create_day(time(10, 0), time(13, 0))

        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=workday,
            tuesday=workday,
            wednesday=workday,
            thursday=workday,
            friday=workday,
            saturday=sat,
            sunday=sun,
        )

    def assign_schedule_to_employee(self, employee, week_start, schedule_dict):
        """Назначение расписания сотруднику"""
        WeekSchedule.objects.create(
            employee=employee,
            start_of_week=week_start,
            monday=schedule_dict['monday'],
            tuesday=schedule_dict['tuesday'],
            wednesday=schedule_dict['wednesday'],
            thursday=schedule_dict['thursday'],
            friday=schedule_dict['friday'],
            saturday=schedule_dict['saturday'],
            sunday=schedule_dict['sunday'],
        )
