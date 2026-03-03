from django.urls import path
from .views import WeeklyScheduleView, UpdateScheduleView, AddEmployeeView, DeleteEmployeeView

urlpatterns = [
    path("weekly/", WeeklyScheduleView.as_view()),
    path("update/", UpdateScheduleView.as_view()),
    path("add/", AddEmployeeView.as_view()),
    path("delete/<int:employee_id>/", DeleteEmployeeView.as_view()),
]
