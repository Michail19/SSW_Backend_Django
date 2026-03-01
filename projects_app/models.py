from django.db import models
from schedule_app.models import Employee


class Project(models.Model):
    project_name = models.CharField(max_length=255, unique=True)

    employees = models.ManyToManyField(
        "schedule_app.Employee",
        through="EmployeeProject",
        related_name="projects"
    )

    def __str__(self):
        return self.project_name


class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("employee", "project")
