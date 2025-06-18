from django.urls import path

from . import views

urlpatterns = [
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/", views.WorkerUpdatedReView.as_view(), name="worker-retrieve"
    ),
    path(
        "processing-carpets/",
        views.ProcessingCarpetListView.as_view(),
        name="processing-carpet-list",
    ),
    path(
        "processing-carpets/<int:pk>/",
        views.ProcessingCarpetUpdatedDestroyView.as_view(),
        name="processing-carpet-list",
    ),
]
