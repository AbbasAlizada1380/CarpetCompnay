from django.urls import path

from .views import RantListCreateView, RantRetrieveUpdateDestroyView

urlpatterns = [
    path("", RantListCreateView.as_view(), name="rant-list-create"),
    path("<int:pk>/", RantRetrieveUpdateDestroyView.as_view(), name="rant-detail"),
]
