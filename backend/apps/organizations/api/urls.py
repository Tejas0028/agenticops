from django.urls import path

from .views import OrganizationListCreateAPIView, OrganizationRetrieveUpdateDeleteAPIView

from apps.departments.api.views import DepartmentListCreateAPIView

urlpatterns = [
    # path("", CreateOrganizationAPIView.as_view(), name="organization-create"),
    path("", OrganizationListCreateAPIView.as_view(), name="organization-list-create"),
    path("<slug:slug>/", OrganizationRetrieveUpdateDeleteAPIView.as_view(), name="organization-detail"),

    # Department create and list routes
    path("<slug:slug>/departments/", DepartmentListCreateAPIView.as_view(), name="department-list-create"),
]
