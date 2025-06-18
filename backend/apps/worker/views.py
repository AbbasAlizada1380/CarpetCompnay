from rest_framework import generics

from .models import ProcessingCarpet, Worker
from .serializers import ProcessingCarpetSerializer, WorkerSerializer


class ProcessingCarpetListView(generics.ListCreateAPIView):
    queryset = ProcessingCarpet.objects.all()
    serializer_class = ProcessingCarpetSerializer


class WorkerListView(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
