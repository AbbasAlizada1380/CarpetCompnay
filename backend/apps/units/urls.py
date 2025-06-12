# apps/units/urls.py
from django.urls import path

from . import views

app_name = "units"

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FinanceViewSet

router = DefaultRouter()
router.register("finances", FinanceViewSet)


urlpatterns = [
    path("", views.UnitListCreateAPIView.as_view(), name="unit-list-create"),
    path(
        "<int:pk>/",
        views.UnitRetrieveUpdateDestroyAPIView.as_view(),
        name="unit-detail",
    ),
    path("bills/", views.UnitBillListCreateView.as_view(), name="unitbill-list-create"),
    path(
        "bills/<int:pk>/",
        views.UnitBillRetrieveUpdateDestroyView.as_view(),
        name="unitbill-detail",
    ),
    
    path("", include(router.urls)),

]
