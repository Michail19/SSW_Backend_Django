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


class DaySchedule(models.Model):
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    def __str__(self):
        if self.start and self.end:
            return f"{self.start}-{self.end}"
        return "Off"

class WeekSchedule(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="week_schedules"
    )

    start_of_week = models.DateField()

    monday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    tuesday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    wednesday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    thursday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    friday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    saturday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")
    sunday = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = ("employee", "start_of_week")


class CurrentWeek(models.Model):
    week_range = models.CharField(max_length=50)
