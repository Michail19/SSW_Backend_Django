from rest_framework import serializers
from .models import DaySchedule, WeekSchedule, Employee


class DayScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaySchedule
        fields = ["start", "end"]


class WeekScheduleSerializer(serializers.ModelSerializer):
    monday = DayScheduleSerializer(required=False)
    tuesday = DayScheduleSerializer(required=False)
    wednesday = DayScheduleSerializer(required=False)
    thursday = DayScheduleSerializer(required=False)
    friday = DayScheduleSerializer(required=False)
    saturday = DayScheduleSerializer(required=False)
    sunday = DayScheduleSerializer(required=False)

    class Meta:
        model = WeekSchedule
        fields = [
            "start_of_week",
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"
        ]


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    week_schedule = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "fio", "projects", "week_schedule"]

    def get_projects(self, obj):
        return " ".join([p.name for p in obj.projects.all()])

    def get_week_schedule(self, obj):
        monday = self.context.get("monday")

        schedule = obj.week_schedules.filter(start_of_week=monday).first()
        if not schedule:
            return None

        return WeekScheduleSerializer(schedule).data
