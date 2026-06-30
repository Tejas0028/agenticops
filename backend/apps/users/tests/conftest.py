import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="tej@example.com",
        first_name="Tej",
        last_name="R",
        password="StrongPassword123",
    )
