from django.urls import path

from .views import ServiceCreateView, ServiceRetrieveUpdateDestroyView

urlpatterns = [
    path("", ServiceCreateView.as_view(), name="service-list-create"),
    path(
        "<int:pk>/",
        ServiceRetrieveUpdateDestroyView.as_view(),
        name="service-detail",
    ),
]
