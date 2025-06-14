from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ExportCarpet
from .serializers import ExportCarpetSerializer


class ExportCarpetViewSet(viewsets.ModelViewSet):
    serializer_class = ExportCarpetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExportCarpet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
