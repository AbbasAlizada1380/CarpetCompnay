from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Services
from .serializers import ServiceSerializer


class ServiceCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save()


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
