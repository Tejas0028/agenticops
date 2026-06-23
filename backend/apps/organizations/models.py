from django.db import models
from apps.common.models import TimeStampedModel
from django.conf import settings


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organizations"

    def __str__(self):
        return self.name
    

class Membership(TimeStampedModel):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user} - {self.organization}"
