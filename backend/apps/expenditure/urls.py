from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExpenditureListCreateAPIView.as_view(), name='expenditure-list'),  # List and create expenditures
    path("<int:pk>/", views.ExpenditureRetrieveUpdateDestroyAPIView.as_view(), name='expenditure-detail'),  # Retrieve, update, delete expenditure
    path("income/", views.IncomeListCreateAPIView.as_view(), name="income"),  # List and create income
    path("income/<int:pk>/", views.IncomeRetrieveUpdateDestroyAPIView.as_view(), name='income-detail'),  # Retrieve, update, delete income
]