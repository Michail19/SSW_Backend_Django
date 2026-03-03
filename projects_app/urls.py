from django.urls import path
from .views import (
    ProjectDetailView,
    ProjectListView,
    ChangeProjectEmployeeView
)

urlpatterns = [
    path("<int:project_id>/", ProjectDetailView.as_view()),
    path("all/", ProjectListView.as_view()),
    path("change/", ChangeProjectEmployeeView.as_view()),
]
