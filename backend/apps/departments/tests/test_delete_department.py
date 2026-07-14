import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.organizations.models import Membership
from apps.departments.models import Department, DepartmentMembership

User = get_user_model()


@pytest.mark.django_db
def test_owner_can_archive_department(
    authenticated_client,
    department,
):
    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    department.refresh_from_db()

    assert department.is_active is False


@pytest.mark.django_db
def test_admin_can_archive_department(
    department,
):
    admin = User.objects.create_user(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="StrongPassword123",
    )

    Membership.objects.create(
        user=admin,
        organization=department.organization,
        role=Membership.Role.ADMIN,
    )

    client = APIClient()

    refresh = RefreshToken.for_user(admin)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
    )

    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    department.refresh_from_db()

    assert department.is_active is False


@pytest.mark.django_db
def test_department_manager_can_archive_department(
    department,
):
    manager = User.objects.create_user(
        email="manager@example.com",
        first_name="Department",
        last_name="Manager",
        password="StrongPassword123",
    )

    organization_membership = Membership.objects.create(
        user=manager,
        organization=department.organization,
        role=Membership.Role.MEMBER,
    )

    DepartmentMembership.objects.create(
        department=department,
        organization_membership=organization_membership,
        role=DepartmentMembership.Role.MANAGER,
    )

    client = APIClient()

    refresh = RefreshToken.for_user(manager)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
    )

    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    department.refresh_from_db()

    assert department.is_active is False


@pytest.mark.django_db
def test_member_cannot_archive_department(
    department,
):
    member = User.objects.create_user(
        email="member@example.com",
        first_name="Member",
        last_name="User",
        password="StrongPassword123",
    )

    Membership.objects.create(
        user=member,
        organization=department.organization,
        role=Membership.Role.MEMBER,
    )

    client = APIClient()

    refresh = RefreshToken.for_user(member)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
    )

    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    department.refresh_from_db()

    assert department.is_active is True


@pytest.mark.django_db
def test_archive_department_requires_authentication(
    api_client,
    department,
):
    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    department.refresh_from_db()

    assert department.is_active is True


@pytest.mark.django_db
def test_archived_department_not_returned_in_list(
    authenticated_client,
    department,
):
    department.is_active = False
    department.save()

    url = reverse(
        "department-list-create",
        kwargs={
            "slug": department.organization.slug,
        },
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0