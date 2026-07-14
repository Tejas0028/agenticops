from apps.departments.models import Department


class DepartmentSelector:
    """
    Handle read/query logic related to departments.
    """

    @staticmethod
    def list_departments(
        *,
        user,
    ):
        return (
            Department.objects.filter(
                organization__memberships__user=user,
                is_active=True,
            )
            .select_related(
                "organization",
            )
            .distinct()
        )
    

    @staticmethod
    def list_organization_department(
        *,
        organization,
    ):
        return (
            Department.objects.filter(
                organization=organization,
                is_active=True,
            )
            .select_related("organization")
        )