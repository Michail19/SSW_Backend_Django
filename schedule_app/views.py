from datetime import datetime
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeDetailsSerializer
from .serializers import WeekScheduleSerializer
from .services import get_full_schedule_for_week
from .services import get_or_create_week, get_week_start


class WeeklyScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_param = request.GET.get("date")
        date = parse_date(date_param) if date_param else None

        monday, employees = get_full_schedule_for_week(request.user, date)

        serializer = EmployeeDetailsSerializer(
            employees,
            many=True,
            context={"monday": monday}
        )

        return Response({
            "currentWeek": monday.strftime("%d-%m %B %Y"),
            "employees": serializer.data
        })


class UpdateScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id):
        employee = Employee.objects.get(id=employee_id)

        date_param = request.data.get("date")
        date = datetime.strptime(date_param, "%Y-%m-%d").date()
        monday = get_week_start(date)

        week = get_or_create_week(employee, monday)

        serializer = WeekScheduleSerializer(
            week,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
