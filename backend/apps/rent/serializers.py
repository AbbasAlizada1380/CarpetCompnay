# apps/rent/serializers.py

from decimal import Decimal
from rest_framework import serializers
from apps.agreement.models import Agreement # Adjust import if needed
from .models import Rant

class RantSerializer(serializers.ModelSerializer):
    customers_list = serializers.JSONField(read_only=False, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_taken = serializers.SerializerMethodField()
    total_remainder = serializers.SerializerMethodField()
    class Meta:
        model = Rant
        fields = (
            "id",
            "floor",
            "time",
            "year",
            "total",
            "customers_list",
            "total_taken",
            "total_remainder",
            "created_at",
            "updated_at",
        )

        read_only_fields = ('created_at', 'updated_at', 'total')
    def update(self, instance, validated_data):
        instance.floor = validated_data.get("floor", instance.floor)
        instance.time = validated_data.get("time", instance.time)
        instance.year = validated_data.get("year", instance.year)
        customers_data_from_request = validated_data.get("customers_list")
        if customers_data_from_request is not None:
            if not isinstance(instance.customers_list, dict):
                instance.customers_list = {}
            for customer_id, customer_update_data in customers_data_from_request.items():
                if not isinstance(customer_update_data, dict):
                    continue 
                customer_id_str = str(customer_id) # Use string keys for JSON
                existing_customer_data = instance.customers_list.get(customer_id_str, {})
                new_rant = Decimal(str(customer_update_data.get('rant', existing_customer_data.get('rant', 0))))
                new_taken = Decimal(str(customer_update_data.get('taken', existing_customer_data.get('taken', 0))))
                new_remainder = new_rant - new_taken
                updated_data_for_customer = {
                    **existing_customer_data, # Start with existing data (preserves 'shop', etc.)
                    "rant": float(new_rant),    # Update rant
                    "taken": float(new_taken),  # Update taken
                    "remainder": float(new_remainder), # Update remainder
                }
                # --- End Modification ---

                instance.customers_list[customer_id_str] = updated_data_for_customer

        # The model's save method will recalculate 'total' based on the updated list
        instance.save()
        return instance

    # get_total_taken and get_total_remainder remain the same
    def get_total_taken(self, obj):
        if isinstance(obj.customers_list, dict):
            return sum(
                Decimal(str(customer.get("taken", 0)))
                for customer in obj.customers_list.values() if isinstance(customer, dict)
            )
        return Decimal("0.00")

    def get_total_remainder(self, obj):
         if isinstance(obj.customers_list, dict):
            return sum(
                Decimal(str(customer.get("remainder", 0)))
                for customer in obj.customers_list.values() if isinstance(customer, dict)
            )
         return Decimal("0.00")