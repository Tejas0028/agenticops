import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from apps.organizations.models import Organization, Membership


User = get_user_model()


@pytest.mark.django_db
def test_list_organizations_successfully(authenticated_client):
    org1 = Organization.objects.create(
        name="Beta",
        slug="beta",
    )

    org2 = Organization.objects.create(
        name="Alpha",
        slug="alpha"
    )

    Membership.objects.create(
        user = authenticated_client.user,
        organization=org1,
        role=Membership.Role.OWNER,
    )

    Membership.objects.create(
        user=authenticated_client.user,
        organization=org2,
        role=Membership.Role.OWNER,
    )

    response = authenticated_client.get(
        reverse("organization-list-create"),
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2

    assert response.data[0]["name"] == "Alpha"
    assert response.data[1]["name"] == "Beta"



@pytest.mark.django_db
def test_list_organizations_only_returns_users_organizations(authenticated_client):
    my_org = Organization.objects.create(
        name="AgenticOps",
        slug="agentic-ops",
    )

    Membership.objects.create(
        user=authenticated_client.user,
        organization=my_org,
        role=Membership.Role.OWNER,
    )

    other_user = User.objects.create_user(
        email="john@exmple.com",
        first_name="John",
        last_name="Doe",
        password="strongpassword123",
    )

    other_org = Organization.objects.create(
        name="Secreat Company",
        slug = "secreat-company",
    )

    Membership.objects.create(
        user=other_user,
        organization=other_org,
        role=Membership.Role.OWNER,
    )

    response = authenticated_client.get(
        reverse("organization-list-create")
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 1

    assert response.data[0]["name"] == "AgenticOps"
    assert response.data[0]["slug"] == "agentic-ops"


@pytest.mark.django_db
def test_list_organizations_requires_authentication(api_client):    
    response = api_client.get(
        reverse("organization-list-create"),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    