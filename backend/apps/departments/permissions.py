from rest_framework.permissions import BasePermission

from apps.departments.models import DepartmentMembership
from apps.organizations.models import Membership


class IsDepartmentManager(BasePermission):
    """
    Allow access to:
    - Organization Owner
    - Organization Admin
    - Department Manager
    """

    def has_object_permission(self, request, view, obj):
        organization_membership = Membership.objects.filter(
            user=request.user,
            organization=obj.organization
        ).first()

        if not organization_membership:
            return False

        if organization_membership is None:
            return False
        
        if organization_membership.role in (
            Membership.Role.OWNER,
            Membership.Role.ADMIN,
        ):
            return True
        

        department_membership = DepartmentMembership.objects.filter(
            department=obj,
            organization_membership=organization_membership,
            role=DepartmentMembership.Role.MANAGER,
        ).exists()

        return department_membership
     
