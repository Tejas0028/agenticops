import pytest

from apps.organizations.services import OrganizationService
from apps.departments.models import Department


@pytest.fixture
def organization(user):
    return OrganizationService.create_organization(
        user=user,
        name="AgenticOps",
        description="Test organization",
    )


@pytest.fixture
def department(organization):
    return Department.objects.create(
        organization=organization,
        name="Engineering",
        description="Engineering Department",
    )