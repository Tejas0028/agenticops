from django.db import transaction

from rest_framework import serializers

from apps.departments.models import Department, DepartmentMembership
from apps.organizations.models import Membership


class DepartmentService:
    """
    Handle business logic related to departments.
    """

    @staticmethod
    @transaction.atomic
    def create_department(
        *,
        organization,
        user,
        name: str,
        description: str = "",
    ) -> Department:
        
        if Department.objects.filter(
            organization=organization,
            name__iexact=name,
        ).exists():
            raise serializers.ValidationError(
                {
                    "name": (
                        [
                            "A department with this name already exists in this organization."
                        ]
                    )
                }
            )
        
        department = Department.objects.create(
            organization=organization,
            name=name,
            description=description,
        )

        organization_membership = Membership.objects.get(
            user=user,
            organization=organization,
        )

        DepartmentMembership.objects.create(
            department=department,
            organization_membership=organization_membership,
            role=DepartmentMembership.Role.MANAGER,
        )

        return department
    

    @staticmethod
    @transaction.atomic
    def update_department(
        *,
        department: Department,
        name: str,
        description: str,
    ) -> Department:
        
        if (
            Department.objects.filter(
                organization=department.organization,
                name__iexact=name,
            )
            .exclude(
                pk=department.pk
            )
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    "name": (
                        "A department with this name already exists "
                        "in this organization."
                    )
                }
            )

        department.name = name
        department.description = description

        department.save(
            update_fields=[
                "name",
                "description",
            ]
        )

        return department
    

    @staticmethod
    @transaction.atomic
    def archive_department(
        *,
        department: Department,
    ) -> Department:
        
        department.is_active = False

        department.save(
            update_fields=[
                "is_active",
            ]
        )

        return department