from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date, parse_time
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee, DaySchedule
from .permissions import IsOwner
from .serializers import EmployeeDetailsSerializer
from .services import get_full_schedule_for_week, get_or_create_week


class WeeklyScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_param = request.GET.get("date")

        if date_param:
            date_param = date_param.rstrip("/")  # убираем возможный слэш

        date = parse_date(date_param) if date_param else None

        monday, employees = get_full_schedule_for_week(request.user, date)

        serializer = EmployeeDetailsSerializer(
            employees,
            many=True,
            context={"monday": monday}
        )

        # Формат "17-23 march 2025"
        week_str = f"{monday.day}-{monday.day + 6} {monday.strftime('%B %Y').lower()}"

        print(Response({
            "currentWeek": week_str,
            "employees": serializer.data
        }).data)

        return Response({
            "currentWeek": week_str,
            "employees": serializer.data
        })


WEEKDAY_REVERSE_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


class UpdateScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        for item in data:
            employee_id = item["employeeId"]
            week_start = parse_date(item["weekStart"])
            schedule_data = item["schedule"]

            employee = Employee.objects.get(id=employee_id)

            # 🔹 Получаем или создаём неделю
            week_obj = get_or_create_week(employee, week_start)

            # 🔹 Обновляем дни
            for day_name, day_values in schedule_data.items():
                weekday_index = WEEKDAY_REVERSE_MAP[day_name]

                day_obj = DaySchedule.objects.get(
                    week=week_obj,
                    weekday=weekday_index
                )

                start = parse_time(day_values.get("start")) if day_values.get("start") else None
                end = parse_time(day_values.get("end")) if day_values.get("end") else None

                day_obj.start = start
                day_obj.end = end
                day_obj.save()

        return Response({"status": "ok"})


User = get_user_model()


class AddEmployeeView(APIView):
    permission_classes = [IsOwner]

    def post(self, request):
        fio = request.data.get("fio")
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        employee = Employee.objects.create(
            fio=fio,
            user=user
        )

        return Response({
            "id": employee.id,
            "fio": employee.fio
        }, status=status.HTTP_201_CREATED)


class DeleteEmployeeView(APIView):
    permission_classes = [IsOwner]

    def delete(self, request, employee_id):
        employee = Employee.objects.get(id=employee_id)
        employee.delete()

        return Response({"detail": "Deleted"})
