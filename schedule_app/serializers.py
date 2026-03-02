from rest_framework import serializers
from .models import DaySchedule, WeekSchedule, Employee

class DayScheduleSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()

    class Meta:
        model = DaySchedule
        fields = ["weekday", "start", "end"]

    def get_start(self, obj):
        return obj.start.strftime("%H:%M") if obj.start else ""

    def get_end(self, obj):
        return obj.end.strftime("%H:%M") if obj.end else ""


class WeekScheduleSerializer(serializers.ModelSerializer):
    days = DayScheduleSerializer(many=True)

    class Meta:
        model = WeekSchedule
        fields = ["days"]


WEEKDAY_MAP = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    weekSchedule = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "fio", "projects", "weekSchedule"]

    def get_projects(self, obj):
        return " ".join([p.name for p in obj.projects.all()])

    def get_weekSchedule(self, obj):
        monday = self.context.get("monday")

        schedule = obj.week_schedules.filter(
            start_of_week=monday
        ).prefetch_related("days").first()

        # пустая неделя
        empty_week = {
            day: {"start": "", "end": ""}
            for day in WEEKDAY_MAP.values()
        }

        if not schedule:
            return empty_week

        result = empty_week.copy()

        for day in schedule.days.all():
            day_name = WEEKDAY_MAP[day.weekday]
            result[day_name] = {
                "start": day.start.strftime("%H:%M") if day.start else "",
                "end": day.end.strftime("%H:%M") if day.end else "",
            }

        return result
