from django.db import models
from apps.common.models import TimeStampedModel
from apps.organizations.models import Organization,Membership

from django.core.exceptions import ValidationError


class Department(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "departments"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="unique_department_name_per_organization"
            )
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.name}"
    

class DepartmentMembership(TimeStampedModel):
    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        MEMBER = "MEMBER", "Member"
    
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    organization_membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        related_name="department_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    class Meta:
        db_table = "department_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "department",
                    "organization_membership",
                ],
                name="unique_department_membership"
            )
        ]

    def clean(self):
        if(
            self.department.organization_id != self.organization_membership.organization_id
        ):
            raise ValidationError(
                "Department and membership must belong to the same organization."
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def __str__(self):
        return (
            f"{self.organization_membership.user.email}"
            f" - {self.department.name}"
        )
