from django.db import models
from django.conf import settings


class Employee(models.Model):
    fio = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.fio


class DaySchedule(models.Model):
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)


class WeekSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_of_week = models.DateField()

    monday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    tuesday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    wednesday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    thursday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    friday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    saturday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    sunday = models.ForeignKey(DaySchedule, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")


class CurrentWeek(models.Model):
    week_range = models.CharField(max_length=50)
