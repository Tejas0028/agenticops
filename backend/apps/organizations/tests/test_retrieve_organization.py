import pytest

from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.organizations.models import Organization, Membership

User = get_user_model()


@pytest.mark.django_db
def test_retrieve_organization_successfully(authenticated_client, user):
    org = Organization.objects.create(
        name = "AgenticOps",
        slug="agentic-slug",
        description= ""
    )

    Membership.objects.create(
        user = user,
        organization = org,
        role = Membership.Role.OWNER,
    )

    response = authenticated_client.get(
        reverse(
            "organization-detail",
            kwargs={"slug": org.slug}
        ),
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == org.name
    assert response.data["slug"] == org.slug
    assert response.data["description"] == org.description


@pytest.mark.django_db
def test_retrieve_organization_returns_404_for_non_member(authenticated_client):
    other_user = User.objects.create_user(
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        password="StrongPassword123",
    )

    organization = Organization.objects.create(
        name = "Secret Company",
        slug = "secret-company",
        description = "Top Secret"
    )

    Membership.objects.create(
        user=other_user,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    response = authenticated_client.get(
        reverse(
            "organization-detail",
            kwargs={"slug" : organization.slug},
        )
    )
        
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_organization_requires_authentication(api_client):   
    organization = Organization.objects.create(
        name = "AgenticOps",
        slug = "agenticops",
    )

    response = api_client.get(
        reverse("organization-detail", kwargs={"slug" : organization.slug})
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED