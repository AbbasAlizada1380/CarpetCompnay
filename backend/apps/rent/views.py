from rest_framework import generics

from .models import Rant
from .serializers import RantSerializer


class RantListCreateView(generics.ListCreateAPIView):
    queryset = Rant.objects.all()
    serializer_class = RantSerializer

    def perform_create(self, serializer):
        """Override to perform any custom save logic."""
        # Create new rant object
        serializer.save()


class RantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rant.objects.all()
    serializer_class = RantSerializer

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
