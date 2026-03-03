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

    def __str__(self):
        return self.fio


class WeekSchedule(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="week_schedules"
    )
    start_of_week = models.DateField()

    class Meta:
        unique_together = ("employee", "start_of_week")


class DaySchedule(models.Model):
    week = models.ForeignKey(
        WeekSchedule,
        on_delete=models.CASCADE,
        related_name="days"
    )
    weekday = models.IntegerField()  # 0=Mon ... 6=Sun

    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ("week", "weekday")


class CurrentWeek(models.Model):
    week_range = models.CharField(max_length=50)
