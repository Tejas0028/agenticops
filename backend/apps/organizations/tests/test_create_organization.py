import pytest
from django.urls import reverse
from rest_framework import status

from apps.organizations.models import Organization, Membership
# from apps.organizations.api.serializers import CreateOrganizationSerializer


@pytest.mark.django_db
def test_create_organization_succesfully(authenticated_client, user):
    payload = {
        "name": "AgenticOps",
        "description": "AI-powered operations platform",
    }

    response = authenticated_client.post(
        reverse("organization-list-create"),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert Organization.objects.filter(
        name=payload["name"],
    ).exists()

    organization = Organization.objects.get(
        name=payload["name"],
    )

    assert organization.slug == "agenticops"

    membership = Membership.objects.get(
        organization=organization,
    )

    assert membership.user == user
    assert membership.role == Membership.Role.OWNER


@pytest.mark.django_db
def test_create_organization_fails_with_duplicate_name(authenticated_client):
    payload = {
        "name": "AgenticOps",
        "description": "First organization",
    }

    response = authenticated_client.post(
        reverse("organization-list-create"),
        payload,
        format= "json"
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = authenticated_client.post(
        reverse("organization-list-create"),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "name" in response.data

    assert Organization.objects.count() == 1
    assert Membership.objects.count() == 1


@pytest.mark.django_db
def test_create_organization_requires_authentication(api_client):
    payload = {
        "name": "AgenticOps",
        "description": "AI-powered operations platform",
    }

    response = api_client.post(
        reverse("organization-list-create"),
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Organization.objects.count() == 0
    assert Membership.objects.count() == 0