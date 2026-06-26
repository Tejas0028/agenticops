from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager
from apps.common.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


