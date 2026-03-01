from django.urls import path
from .views import WeeklyScheduleView, UpdateScheduleView, AddEmployeeView

urlpatterns = [
    path("weekly/", WeeklyScheduleView.as_view()),
    path("update/<int:employee_id>/", UpdateScheduleView.as_view()),
    path("add/", AddEmployeeView.as_view()),
]
