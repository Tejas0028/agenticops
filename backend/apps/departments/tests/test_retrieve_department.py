import pytest 

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from apps.departments.models import Department
from apps.organizations.services import OrganizationService

User = get_user_model()

@pytest.mark.django_db
def test_retrieve_departmeny_success(
    authenticated_client,
    department
):
    url = reverse (
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == department.id
    assert response.data["name"] == department.name
    assert response.data["description"] == department.description

    assert response.data["organization"] == department.organization.name


@pytest.mark.django_db
def test_user_cannot_retrieve_department_from_another_organization(authenticated_client):
    another_user = User.objects.create(
        email="another@example.com",
        first_name="Another",
        last_name="User",
        password="StrongPassword123",
    )

    another_organization = OrganizationService.create_organization(
        user=another_user,
        name="Another Organization",
        description="Another organization",
    )

    department = Department.objects.create(
        organization=another_organization,
        name="Finance",
        description="Finance Department",
    )

    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_department_requires_authentication(
    api_client,
    department,
):
    url = reverse(
        "department-detail",
        kwargs={
            "id": department.id,
        },
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED