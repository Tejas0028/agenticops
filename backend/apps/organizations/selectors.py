from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.organizations.models import Organization,Membership

User = get_user_model()


class OrganizationSelector:
    """
    Handles read operations for organizations.
    """

    @staticmethod
    def list_organizations(
        *,
        user: User,
    ):
        return(
            Organization.objects.filter(
                memberships__user=user,
                is_active=True,
            )
            .order_by("name")
        )
    

    @staticmethod
    def list_manageable_organizations(
        *,
        user,
    ):
        return Organization.objects.filter(
            memberships__user=user,
            memberships__role__in=[
                Membership.Role.OWNER,
                Membership.Role.ADMIN,
            ],
            is_active=True,
        ).distinct()
        
    

    @staticmethod
    def get_organization(
        *,
        user: User,
        slug: str,
    ) -> Organization:
        return get_object_or_404(
            Organization.objects.filter(
                memberships__user=user,
            ),
            slug=slug,
        )