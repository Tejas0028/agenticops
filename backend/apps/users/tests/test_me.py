import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_current_user_successfully(api_client, user):
    login_response = api_client.post(
        reverse("login"),
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json"
    )

    assert login_response.status_code == status.HTTP_200_OK

    access_token = login_response.data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = api_client.get(
        reverse("me"),
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name


@pytest.mark.django_db
def test_get_current_user_without_token(api_client):
    response = api_client.get(
        reverse("me"),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_current_user_with_invalid_token(api_client):
    api_client.credentials(
        HTTP_AUTHORIZATION="bearer invalid-token",
    )

    response = api_client.get(
        reverse("me"),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

