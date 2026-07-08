from django.urls import path

from .views import OrganizationListCreateAPIView, OrganizationRetrieveUpdateDeleteAPIView

urlpatterns = [
    # path("", CreateOrganizationAPIView.as_view(), name="organization-create"),
    path("", OrganizationListCreateAPIView.as_view(), name="organization-list-create"),
    path("<slug:slug>/", OrganizationRetrieveUpdateDeleteAPIView.as_view(), name="organization-detail"),
]
