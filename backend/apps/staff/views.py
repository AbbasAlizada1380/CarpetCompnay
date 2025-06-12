# views.py
from rest_framework import generics
from .models import Salary, Staff
from .serializers import SalarySerializer, StaffSerializer
# Optional: Add permissions if needed
# from rest_framework.permissions import IsAuthenticated

class StaffListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create Staff members."""
    queryset = Staff.objects.order_by('name') # Use default ordering from model
    serializer_class = StaffSerializer
    # permission_classes = [IsAuthenticated] # Example permission

class StaffRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, and delete a Staff member."""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # permission_classes = [IsAuthenticated] # Example permission

class SalaryListCreateView(generics.ListCreateAPIView):
    """API view to list and create Salary periods."""
    queryset = Salary.objects.order_by('-year', '-month') # Use default ordering
    serializer_class = SalarySerializer
    # permission_classes = [IsAuthenticated] # Example permission

class SalaryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, and delete a Salary period."""
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    # permission_classes = [IsAuthenticated] # Example permission