import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.departments.models import Department, DepartmentMembership
from apps.organizations.models import Membership

User = get_user_model()

@pytest.mark.django_db
def test_update_department_success(authenticated_client, department):
    url = reverse (
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = authenticated_client.patch(
        url,
        {
            "name": "Platform",
            "description": "Platform Team",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    department.refresh_from_db()

    assert department.name == "Platform"
    assert department.description == "Platform Team"

    assert response.data["name"] == "Platform"
    assert response.data["description"] == "Platform Team"


@pytest.mark.django_db
def test_cannot_update_department_with_duplicate_name(
    authenticated_client,
    organization,
    department,
):
    Department.objects.create(
        organization=organization,
        name="Marketing",
        description="Marketing Department",
    )

    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = authenticated_client.patch(
        url,
        {
            "name": "Marketing",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "name" in response.data


@pytest.mark.django_db
def test_update_department_requires_authentication(
    api_client,
    department,
):
    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = api_client.patch(
        url,
        {
            "name": "Platform",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_member_cannot_update_department(organization, department):
    member = User.objects.create_user(
        email="member@example.com",
        first_name="Member",
        last_name="User",
        password="StrongPassword123",
    )

    Membership.objects.create(
        user=member,
        organization=organization,
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

    response = client.patch(
        url,
        {
            "name": "Platform",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_department(
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

    response = client.patch(
        url,
        {
            "name": "Platform",
            "description": "Platform Team",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    department.refresh_from_db()

    assert department.name == "Platform"


@pytest.mark.django_db
def test_department_manager_can_update_department(
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

    response = client.patch(
        url,
        {
            "name": "Platform",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    department.refresh_from_db()

    assert department.name == "Platform"



