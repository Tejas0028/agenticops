from django.db import transaction

from apps.organizations.models import Organization, Membership
from apps.organizations.utils import generate_unique_slug

from rest_framework import serializers


class OrganizationService:
    """
    Handles organization-related business operations.
    """

    @staticmethod
    @transaction.atomic
    def create_organization(
        *,
        user,
        name: str,
        description: str = "",
    ) -> Organization:
        
        if Organization.objects.filter(
            memberships__user=user,
            name__iexact=name,
        ).exists():
            raise serializers.ValidationError(
                {
                    "name": "You already have an organization with this name."
                }
            )
        
        slug = generate_unique_slug(name)
        
        organization = Organization.objects.create(
            name=name,
            slug=slug,
            description=description,
        )

        Membership.objects.create(
            user=user,
            organization=organization,
            role=Membership.Role.OWNER,
        )

        return organization
    

    @staticmethod
    @transaction.atomic
    def archive_organization(
        *,
        organization: Organization,
    ) -> Organization:
        
        organization.is_active = False

        organization.save(
            update_fields=[
                "is_active"
            ]
        )
        return organization
    

    @staticmethod
    @transaction.atomic
    def update_organization(
        *,
        user,
        organization: Organization,
        name: str,
        description: str,
    ) -> Organization:
        
        if(
            Organization.objects.filter(
                memberships__user=user,
                name__iexact=name,
            )
            .exclude(pk=organization.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    "name": ["You already have an organization with this name."]
                }
            )
        
        organization.name = name
        organization.description = description

        organization.save(
            update_fields=[
                "name",
                "description",
            ]
        )

        return organization