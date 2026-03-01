from rest_framework import serializers
from .models import DaySchedule, WeekSchedule, Employee

class DayScheduleSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()

    class Meta:
        model = DaySchedule
        fields = ["start", "end"]

    def get_start(self, obj):
        return obj.start.strftime("%H:%M") if obj.start else ""

    def get_end(self, obj):
        return obj.end.strftime("%H:%M") if obj.end else ""


class WeekScheduleSerializer(serializers.ModelSerializer):
    monday = DayScheduleSerializer()
    tuesday = DayScheduleSerializer()
    wednesday = DayScheduleSerializer()
    thursday = DayScheduleSerializer()
    friday = DayScheduleSerializer()
    saturday = DayScheduleSerializer()
    sunday = DayScheduleSerializer()

    class Meta:
        model = WeekSchedule
        fields = [
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"
        ]


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

        schedule = obj.week_schedules.filter(start_of_week=monday).first()
        if not schedule:
            # возвращаем пустую неделю
            empty_week = {day: {"start": "", "end": ""} for day in
                          ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}
            return empty_week
        return WeekScheduleSerializer(schedule).data
