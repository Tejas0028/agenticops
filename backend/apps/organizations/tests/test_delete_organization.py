import pytest

from django.urls import reverse
from rest_framework import status

from apps.organizations.models import Membership, Organization
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_owner_can_archive_organization(
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

    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    organization.refresh_from_db()

    assert organization.is_active is False


@pytest.mark.django_db
def test_admin_can_archive_organization(
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
        role=Membership.Role.ADMIN,
    )

    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    organization.refresh_from_db()

    assert organization.is_active is False



@pytest.mark.django_db
def test_member_cannot_archive_organization(
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
        role=Membership.Role.MEMBER,
    )

    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    organization.refresh_from_db()

    assert organization.is_active is True


@pytest.mark.django_db
def test_non_member_cannot_archive_organization(
    api_client,
    user,
):
    owner = User.objects.create_user(
        email="owner@example.com",
        first_name="Owner",
        last_name="User",
        password="StrongPassword123",
    )

    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
    )

    Membership.objects.create(
        user=owner,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_anonymous_user_cannot_archive_organization(
    api_client,
):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
    )

    response = api_client.delete(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_archived_organization_is_not_listed(
    api_client,
    user,
):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        is_active=False,
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse("organization-list-create"),
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 0


@pytest.mark.django_db
def test_archived_organization_cannot_be_retrieved(
    api_client,
    user,
):
    organization = Organization.objects.create(
        name="AgenticOps",
        slug="agenticops",
        is_active=False,
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role=Membership.Role.OWNER,
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse(
            "organization-detail",
            kwargs={
                "slug": organization.slug,
            },
        )
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND