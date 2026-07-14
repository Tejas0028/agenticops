import pytest
from django.urls import reverse

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from apps.organizations.models import Membership
from apps.departments.models import Department, DepartmentMembership

from apps.organizations.services import OrganizationService

User = get_user_model()



@pytest.mark.django_db
def test_create_department_success(authenticated_client, organization):
    url = reverse(
        "department-list-create",
        kwargs={
            "slug": organization.slug
        },
    )

    data = {
        "name": "Engineering",
        "description": "Engineering Department",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    department = Department.objects.get(
        organization=organization,
        name="Engineering",
    )

    assert department.description == "Engineering Department"

    assert response.data["name"] == "Engineering"
    assert response.data["description"] == "Engineering Department"
    assert response.data["organization"] == organization.name


@pytest.mark.django_db
def test_cannot_create_duplicate_department_name(authenticated_client, organization):
    department = Department.objects.create(
        organization=organization,
        name="Engineering",
        description="Engineering Department",
    )

    url = reverse(
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    response = authenticated_client.post(
        url,
        {
            "name": "Engineering",
            "description": "Duplicate",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "name" in response.data

    assert (response.data["name"][0] == "A department with this name already exists in this organization.")



@pytest.mark.django_db
def test_create_department_requires_authentication(api_client, organization):
    url = reverse(
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    respose = api_client.post(
        url,
        {
            "name": "Engineering",
            "description": "Engineering Department",
        },
        format="json"
    )

    assert respose.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_organization_member_cannot_create_department(organization):
    member = User.objects.create(
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
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    url = reverse(
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    response = client.post(
        url,
        {
            "name": "Engineering",
            "description": "Engineering Department",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_same_department_name_allowed_in_different_organizations(authenticated_client, user, organization):
    Department.objects.create(
        organization=organization,
        name="Engineering",
        description="Engineering Department",
    )

    second_organization = OrganizationService.create_organization(
        user=user,
        name="Second Organization",
        description="Another Organization"
    )

    url = reverse(
        "department-list-create",
        kwargs={
            "slug": second_organization.slug,
        },
    )

    response = authenticated_client.post(
        url,
        {
            "name": "Engineering",
            "description": "Engineering Department",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert Department.objects.filter(
        organization=second_organization,
        name="Engineering",
    ).exists()


@pytest.mark.django_db
def test_creator_becomes_department_manager(
    authenticated_client,
    user,
    organization,
):
    url = reverse (
        "department-list-create",
        kwargs={
            "slug": organization.slug,
        },
    )

    response = authenticated_client.post(
        url,
        {
            "name": "Engineering",
            "description": "Engineering Department",
        },
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED

    department = Department.objects.get(
        organization=organization,
        name="Engineering"
    )

    organization_membership = Membership.objects.get(
        user=user,
        organization=organization,
    )

    assert DepartmentMembership.objects.filter(
        department=department,
        organization_membership=organization_membership,
        role=DepartmentMembership.Role.MANAGER
    ).exists()