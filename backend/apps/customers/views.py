from rest_framework import generics, status
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.attachment:
             instance.attachment.delete(save=False) 
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

