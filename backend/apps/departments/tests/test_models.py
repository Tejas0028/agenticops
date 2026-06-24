from django.test import TestCase

from apps.departments.models import Department,DepartmentMembership
from apps.organizations.models import Organization,Membership
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()



class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        organization = Organization.objects.create(
            name="Test Org",
            slug="test-org"
        )

        department = Department.objects.create(
            organization=organization,
            name="Engineering",
        )

        self.assertEqual(
            department.name,
            "Engineering"
        )


    def test_department_membership_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        organization = Organization.objects.create(
            name="Test Org",
            slug="test-org"
        )

        membership = Membership.objects.create(
            user=user,
            organization=organization,
            role=Membership.Role.OWNER
        )

        department = Department.objects.create(
            organization=organization,
            name="Engineering",
        )

        department_membership = DepartmentMembership.objects.create(
            department=department,
            organization_membership = membership
        )

        self.assertEqual(
            department_membership.organization_membership.user.username,
            "testuser",
        )

    def test_department_membership_must_belong_to_same_organization(self):
        org1 = Organization.objects.create(
            name="Organization One",
            slug="organization-one"
        )

        org2 = Organization.objects.create(
            name="Organization Two",
            slug="organization-two"
        )

        department = Department.objects.create(
            organization=org1,
            name="Engineering"
        )

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        membership = Membership.objects.create(
            user=user,
            organization=org2,
            role=Membership.Role.MEMBER
        )

        with self.assertRaises(ValidationError):
            DepartmentMembership.objects.create(
                department=department,
                organization_membership=membership,
            )
