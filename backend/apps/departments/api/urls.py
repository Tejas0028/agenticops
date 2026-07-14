from django.urls import path

from .views import DepartmentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("<int:id>/", DepartmentRetrieveUpdateDestroyAPIView.as_view(), name="department-detail"),
]
