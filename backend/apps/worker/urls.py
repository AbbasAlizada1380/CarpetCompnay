from django.urls import path

from . import views

urlpatterns = [
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path(
        "processing-carpets/",
        views.ProcessingCarpetListView.as_view(),
        name="processing-carpet-list",
    ),
]
