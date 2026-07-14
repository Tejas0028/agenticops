import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from apps.departments.models import Department
from apps.organizations.services import OrganizationService

User = get_user_model()

@pytest.mark.django_db
def test_list_department_success(authenticated_client, organization):
    Department.objects.create(
        organization=organization,
        name = "Engineering",
        description="Engineering Department"
    )

    Department.objects.create(
        organization=organization,
        name="Marketing",
        description="Marketing Department",
    )

    url = reverse(
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2

    names = [
        department["name"]
        for department in response.data
    ]

    assert "Engineering" in names
    assert "Marketing" in names


@pytest.mark.django_db
def test_user_only_sees_departments_from_their_organizations(authenticated_client, organization):
    # User's organization
    Department.objects.create(
        organization=organization,
        name="Engineering",
        description="Engineering Department",
    )

    #Another user
    another_user = User.objects.create_user(
        email="another@example.com",
        first_name="Another",
        last_name="User",
        password="StrongPassword123",
    )

    # Another organization
    another_organization = OrganizationService.create_organization(
        user=another_user,
        name="Another Organization",
        description="Another organization",
    )

    Department.objects.create(
        organization=another_organization,
        name="Finance",
        description="Finance Department",
    )
    
    url = reverse(
        "department-list-create",
        kwargs={
            "slug": another_organization.slug,
        },
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    # assert len(response.data) == 1

    # assert response.data[0]["name"] == "Engineering"



@pytest.mark.django_db
def test_list_departments_requires_authentication(api_client, organization):
    url = reverse (
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED