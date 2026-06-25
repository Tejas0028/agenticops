from django.core.exceptions import ValidationError

from django.db import models
from apps.common.models import TimeStampedModel
from apps.organizations.models import Organization
from apps.departments.models import Department,DepartmentMembership


class Goal(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
    
    class Priority(models.TextChoices):
        LOW = 'LOW', "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="goals",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="goals",
    )

    owner = models.ForeignKey(
        DepartmentMembership,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_goals"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "goals"
    
    def __str__(self):
        return self.title
    

    def clean(self):
        if self.department.organization_id != self.organization_id:
            raise ValidationError(
                "Department must belong to the selected organization."
            )
        
        if self.owner and self.owner.department_id != self.organization_id:
            raise ValidationError(
                "Goal owner must belong to the same organization."
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)