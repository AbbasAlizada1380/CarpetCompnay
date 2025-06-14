from django.urls import path

from . import views

urlpatterns = [
    path(
        "income/", views.IncomeListCreateAPIView.as_view(), name="income"
    ),  # List and create income
    path(
        "income/<int:pk>/",
        views.IncomeRetrieveUpdateDestroyAPIView.as_view(),
        name="income-detail",
    ),  # Retrieve, update, delete income
]
