from django.shortcuts import render
from rest_framework import generics

from .models import Expenditure, Income
from .serializers import ExpenditureSerializer, IncomeSerializer


class ExpenditureListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer


class ExpenditureRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer


class IncomeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
