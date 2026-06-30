import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_login_successful(api_client, user):
    payload = {
        "email" : user.email,
        "password" : "StrongPassword123",
    }

    response = api_client.post(
        reverse("login"),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert "access" in response.data
    assert "refresh" in response.data
    assert "user" in response.data

    assert response.data["user"]["email"] == user.email


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email,password",
    [
        ("tej@example.com", "WrongPassword123"),
        ("unknown@example.com", "StrongPassword123"),
        ("unknown@example.com", "WrongPassword123"),
    ],
)

def test_login_fails_with_invalid_credentials(
    api_client,
    user,
    email,
    password,
):
    payload = {
        "email": email,
        "password": password,
    }

    response = api_client.post(
        reverse("login"),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data