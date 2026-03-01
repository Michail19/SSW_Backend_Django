from rest_framework import serializers
from schedule_app.models import Employee
from .models import Project


class EmployeeLessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "fio"]


class ProjectSerializer(serializers.ModelSerializer):
    employees = EmployeeLessSerializer(many=True)

    class Meta:
        model = Project
        fields = ["name", "employees"]


class EmployeeProjectsSerializer(serializers.Serializer):
    action = serializers.CharField()
    project = serializers.CharField()
    fio = EmployeeLessSerializer(many=True)
