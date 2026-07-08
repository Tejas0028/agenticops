from rest_framework.permissions import BasePermission

from apps.organizations.models import Membership


class IsOrganizationAdminOrOwner(BasePermission):
    """
    Allows access only to organization owners and admins.
    """

    def has_object_permission(self, request, view, obj):
        membership = Membership.objects.filter(
            user = request.user,
            organization = obj,
        ).first()

        if membership is None:
            return False
        
        return membership.role in (
            Membership.Role.OWNER,
            Membership.Role.ADMIN,
        )