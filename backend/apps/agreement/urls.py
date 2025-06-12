from django.urls import path

from . import views

urlpatterns = [
    path("agreements/", views.AgreementList.as_view(), name="agreement-list"),
    path(
        "agreements/<int:pk>/", views.AgreementDetail.as_view(), name="agreement-detail"
    ),
]
