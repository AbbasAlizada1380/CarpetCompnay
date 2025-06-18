from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ExportCarpet, ImportCarpet
from .paginations import CustomPageNumberPagination
from .serializers import ExportCarpetSerializer, ImportCarpetSerializer


class ExportCarpetViewSet(viewsets.ModelViewSet):
    serializer_class = ExportCarpetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return ExportCarpet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImportCarpetViewSet(viewsets.ModelViewSet):
    serializer_class = ImportCarpetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return ImportCarpet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
