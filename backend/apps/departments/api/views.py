from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.departments.selectors import DepartmentSelector
from apps.departments.services import DepartmentService
from apps.departments.api.serializers import DepartmentSerializer, CreateDepartmentSerializer, UpdateDepartmentSerializer

from apps.organizations.selectors import OrganizationSelector

from apps.departments.permissions import IsDepartmentManager


class DepartmentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization = get_object_or_404(
            OrganizationSelector.list_organizations(
                user=self.request.user
            ),
            slug=self.kwargs["slug"],
        )

        return DepartmentSelector.list_organization_department(
            organization=organization,
        )
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateDepartmentSerializer
        
        return DepartmentSerializer
    
    def create(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationSelector.list_manageable_organizations(
                user=self.request.user
            ),
            slug=self.kwargs["slug"],
        )

        serializer = self.get_serializer(
            data=request.data,
            context={
                "organization": organization,
                "user": request.user,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        department = serializer.save()

        return Response(
            DepartmentSerializer(department).data,
            status=status.HTTP_201_CREATED,
        )
    

class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        return DepartmentSelector.list_departments(
            user=self.request.user,
        )
    
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateDepartmentSerializer
        
        return DepartmentSerializer
    
    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE",):
            permission_classes = [
                IsAuthenticated,
                IsDepartmentManager,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]
    
    def perform_destroy(self, instance):
        DepartmentService.archive_department(
            department=instance,
        )