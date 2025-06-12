from django.urls import path

from .views import (
    SalaryListCreateView,
    SalaryRetrieveUpdateDestroyView,
    StaffListCreateAPIView,
    StaffRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("staff/", StaffListCreateAPIView.as_view(), name="staff-list-create"),
    path(
        "staff/<int:pk>/",
        StaffRetrieveUpdateDestroyAPIView.as_view(),
        name="staff-detail",
    ),
    path("salaries/", SalaryListCreateView.as_view(), name="salary-list-create"),
    path(
        "salaries/<int:pk>/",
        SalaryRetrieveUpdateDestroyView.as_view(),
        name="salary-retrieve-update-destroy",
    ),
]
