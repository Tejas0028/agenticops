from rest_framework import status
# from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CreateOrganizationSerializer, OrganizationSerializer, UpdateOrganizationSerializer
from apps.organizations.selectors import OrganizationSelector
from apps.organizations.permissions import IsOrganizationAdminOrOwner
from apps.organizations.services import OrganizationService


# class CreateOrganizationAPIView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CreateOrganizationSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(
#             data=request.data,
#         )

#         serializer.is_valid(
#             raise_exception=True,
#         )

#         organization = serializer.save()

#         return Response(
#             OrganizationSerializer(organization).data,
#             status=status.HTTP_201_CREATED,
#         )
    

# class ListOrganizationAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrganizationSerializer

#     def get(self):
#         return OrganizationSelector.list_organizations(
#             user=self.request.user,
#         )


class OrganizationListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrganizationSerializer
        
        return OrganizationSerializer
    
    def get_queryset(self):
        return OrganizationSelector.list_organizations(
            user=self.request.user,
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = serializer.save()

        return Response(
            OrganizationSerializer(organization).data,
            status=status.HTTP_201_CREATED
        )
    


# class OrganizationRetrieveAPIView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrganizationSerializer
#     lookup_field = "slug"

#     def get_queryset(self):
#         return OrganizationSelector.list_organizations(
#             user=self.request.user,
#         )
    

# class OrganizationUpdateAPIView(UpdateAPIView):
#     permission_classes  = [IsAuthenticated, IsOrganizationAdminOrOwner]
#     serializer_class = UpdateOrganizationSerializer
#     lookup_field = "slug"

#     def get_queryset(self):
#         return OrganizationSelector.list_organizations(
#             user=self.request.user
#         )


class OrganizationRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"

    def get_queryset(self):
        return OrganizationSelector.list_organizations(
            user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateOrganizationSerializer
        
        return OrganizationSerializer
    
    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            permission_classes = [
                IsAuthenticated,
                IsOrganizationAdminOrOwner,
            ]
        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        organization = serializer.save()
        
        return Response(
            OrganizationSerializer(
                organization
            ).data,
            status=status.HTTP_200_OK,
        )
    
    def perform_destroy(self, instance):
        OrganizationService.archive_organization(
            organization=instance,
        )


# class OrganizationDestroyAPIView(DestroyAPIView):
#     permission_classes = [
#         IsAuthenticated,
#         IsOrganizationAdminOrOwner,
#     ]

#     lookup_field = "slug"

#     def get_queryset(self):
#         return OrganizationSelector.list_organizations(
#             user=self.request.user,
#         )
    
#     def perform_destroy(self, instance):
#         OrganizationService.archive_organization(
#             organization=instance,
#         )