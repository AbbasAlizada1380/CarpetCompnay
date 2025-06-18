from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import ExportCarpetViewSet

router = DefaultRouter()
router.register("carpets", ExportCarpetViewSet, basename="carpet")
router.register("import", ExportCarpetViewSet, basename="import")

urlpatterns = [
    path("", include(router.urls)),
]
