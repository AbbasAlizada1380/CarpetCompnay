# apps/expenditure/serializers.py
from rest_framework import serializers
from decimal import Decimal # Import Decimal
from .models import  Income


class IncomeSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Income
        fields = [
            "id",
            "source",
            "amount",
            "description",
            "month",
            "year",
            "receiver",
            "consumer", 
            "total_amount", 
            "created_at",
            "updated_at",
        ]
        read_only_fields = ('created_at', 'updated_at', 'total_amount')

    def get_total_amount(self, obj):
        total = Income.calculate_total_amount()
        return float(total) if total is not None else 0.0
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['amount'] = float(instance.amount) if instance.amount is not None else 0.0
        return data