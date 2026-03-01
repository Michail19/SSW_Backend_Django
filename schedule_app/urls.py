from django.urls import path
from .views import WeeklyScheduleView, UpdateScheduleView

urlpatterns = [
    path("weekly/", WeeklyScheduleView.as_view()),
    path("update/<int:employee_id>/", UpdateScheduleView.as_view()),
]
