from django.db import models
from django.conf import settings


class Employee(models.Model):
    fio = models.CharField(max_length=255)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        blank=True
    )

    projects = models.ManyToManyField("projects_app.Project", blank=True)

    def __str__(self):
        return self.fio


class DaySchedule(models.Model):
    start = models.CharField(max_length=10, null=True, blank=True)
    end = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.start}-{self.end}"


class WeekSchedule(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="week_schedules"
    )

    start_of_week = models.DateField()

    monday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    tuesday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    wednesday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    thursday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    friday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    saturday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")
    sunday = models.OneToOneField(DaySchedule, on_delete=models.SET_NULL, null=True, related_name="+")

    class Meta:
        unique_together = ("employee", "start_of_week")


class CurrentWeek(models.Model):
    week_range = models.CharField(max_length=50)
