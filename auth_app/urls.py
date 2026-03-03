from django.urls import path
from .views import LoginView, VerifyView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("verify/", VerifyView.as_view()),
]
