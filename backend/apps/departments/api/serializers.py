from rest_framework import serializers

from apps.departments.models import Department
from apps.departments.services import DepartmentService


class DepartmentSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Department
        fields = [
            "id",
            "organization",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields



class CreateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def create(self, validated_data):
        return DepartmentService.create_department(
            organization=self.context["organization"],
            user=self.context["user"],
            **validated_data,
        )
    

class UpdateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=False,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def update(self, instance, validated_data):
        return DepartmentService.update_department(
            department=instance,
            name=validated_data.get(
                "name",
                instance.name,
            ),
            description=validated_data.get(
                "description",
                instance.description,
            ),
        )