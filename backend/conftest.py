import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.organizations.models import Membership

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


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    return api_client