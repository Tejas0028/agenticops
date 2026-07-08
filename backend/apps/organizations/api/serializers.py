from rest_framework import serializers

from apps.organizations.models import Organization, Membership
from apps.organizations.services import OrganizationService


class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )


    def create(self, validated_data):
        return OrganizationService.create_organization(
            user=self.context["request"].user,
            **validated_data,
        )
    

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class UpdateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length = 255,
        required = False,
    )

    description = serializers.CharField(
        required = False,
        allow_blank = True,
    )

    def update(self, instance, validated_data):
        return OrganizationService.update_organization(
            user=self.context["request"].user,
            organization=instance,
            name=validated_data.get(
                "name",
                instance.name,
            ),
            description=validated_data.get(
                "description",
                instance.description,
            ),
        )