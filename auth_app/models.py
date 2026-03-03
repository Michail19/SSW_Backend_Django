from django.contrib.auth.models import AbstractUser
from django.db import models


class AccessLevel(models.TextChoices):
    USER = "USER"
    OWNER = "OWNER"


class User(AbstractUser):
    level = models.CharField(
        max_length=10,
        choices=AccessLevel.choices,
        default=AccessLevel.USER
    )
