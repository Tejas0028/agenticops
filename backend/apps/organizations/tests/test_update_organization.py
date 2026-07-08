import pytest

from django.urls import reverse
from rest_framework import status

from apps.organizations.models import Membership, Organization

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_owner_can_update_organization(api_client, user):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        description="Old description",
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(
        user=user,
    )

    payload = {
        "name": "AgenticOps AI",
        "description": "New description",
    }

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs=
            {
                "slug": organization.slug
            },
        ),
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK

    organization.refresh_from_db()

    assert organization.name == "AgenticOps AI"
    assert organization.description == "New description"

    assert organization.slug == "agenticops"

    assert response.data["name"] == "AgenticOps AI"
    assert response.data["slug"] == "agenticops"


@pytest.mark.django_db
def test_admin_can_update_organization(api_client, user):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        description="Old description",
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.ADMIN,
    )

    api_client.force_authenticate(
        user=user,
    )

    payload = {
        "name": "AgenticOps AI",
        "description": "Updated description",
    }

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        ),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    organization.refresh_from_db()

    assert organization.name == "AgenticOps AI"
    assert organization.description == "Updated description"
    assert organization.slug == "agenticops"


@pytest.mark.django_db
def test_member_cannot_update_organization(api_client, user):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        description="Old description",
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.MEMBER,
    )

    api_client.force_authenticate(
        user=user,
    )

    payload = {
        "name": "AgenticOps AI",
    }

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug
            },
        ),
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    organization.refresh_from_db()

    assert organization.name == "AgenticOps"
    assert organization.description == "Old description"
    assert organization.slug == "agenticops"


@pytest.mark.django_db
def test_non_member_gets_404(api_client, user): 
    owner = User.objects.create_user(
        email="owner@example.com",
        first_name="Owner",
        last_name="User",
        password="StrongPassword123",
    )

    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        description="Old description",
    )

    Membership.objects.create(
        user=owner,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(
        user=user,
    )

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        ),
        {
            "name": "New Name",
        },
        format="json"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    organization.refresh_from_db()

    assert organization.name == "AgenticOps"


@pytest.mark.django_db
def test_update_organization_fails_with_duplicate_name(
    api_client,
    user,
):
    first = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
    )

    second = Organization.objects.create(
        name="AI Studio",
        slug="ai-studio",
    )

    Membership.objects.create(
        user=user,
        organization=first,
        role=Membership.Role.OWNER,
    )

    Membership.objects.create(
        user=user,
        organization=second,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(
        user=user,
    )

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": second.slug,
            },
        ),
        {
            "name": "AgenticOps",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    second.refresh_from_db()

    assert second.name == "AI Studio"

    assert response.data == {
        "name": [
            "You already have an organization with this name."
        ]
    }


@pytest.mark.django_db
def test_slug_does_not_change(
    api_client,
    user,
):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(
        user=user,
    )

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        ),
        {
            "name": "AgenticOps AI",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    organization.refresh_from_db()

    assert organization.slug == "agenticops"


@pytest.mark.django_db
def test_anonymous_user_cannot_update_organization(
    api_client,
):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
    )

    response = api_client.patch(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        ),
        {
            "name": "New Name",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED