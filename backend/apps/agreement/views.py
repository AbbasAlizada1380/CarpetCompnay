from rest_framework import generics, status
from rest_framework.response import Response

from .models import Agreement
from .serializers import AgreementSerializer


class AgreementList(generics.ListCreateAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer

    def perform_create(self, serializer):
        serializer.save()


class AgreementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
