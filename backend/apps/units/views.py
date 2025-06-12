# apps/units/views.py
from rest_framework import generics, viewsets

from .models import Finance, Unit, UnitBill
from .serializers import FinanceSerializer, UnitBillSerializer, UnitSerializer


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer


# --- Views for Managing Individual Units ---
class UnitListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create Units."""

    # Remove select_related('customer') as customer is no longer a relation
    queryset = Unit.objects.order_by("unit_number")
    serializer_class = UnitSerializer
    # permission_classes = [IsAuthenticated]


class UnitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, and delete a Unit."""

    # Remove select_related('customer')
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    # permission_classes = [IsAuthenticated]


# --- Views for Managing Monthly Unit Bills ---
class UnitBillListCreateView(generics.ListCreateAPIView):
    """API view to list and create Unit Bill periods."""

    queryset = UnitBill.objects.order_by("-year", "-month")  # Use default ordering
    serializer_class = UnitBillSerializer
    # permission_classes = [IsAuthenticated]


class UnitBillRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, and delete a Unit Bill period."""

    queryset = UnitBill.objects.all()
    serializer_class = UnitBillSerializer
    # permission_classes = [IsAuthenticated]
