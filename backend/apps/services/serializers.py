
from decimal import Decimal
from rest_framework import serializers
from .models import Services
# Remove Agreement import if not directly needed here

class ServiceSerializer(serializers.ModelSerializer):
    # Make customers_list writeable for updates, but not required on create
    customers_list = serializers.JSONField(read_only=False, required=False)
    # Make total read-only as it's calculated by the model's save method
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # Add dynamic fields for total_taken and total_remainder
    total_taken = serializers.SerializerMethodField()
    total_remainder = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = (
            "id",
            "floor",
            "time",
            "year",
            "total",        # Total service fee for the floor/time
            "is_approved",  # Overall approval status
            "customers_list", # Details per customer
            "total_taken",    # Calculated dynamically
            "total_remainder",# Calculated dynamically
            "created_at",
            "updated_at",
        )
        # Add read_only_fields similar to rent app
        read_only_fields = ('created_at', 'updated_at', 'total')

    def get_total_taken(self, obj):
        """Calculate total taken amount from the customers_list."""
        if isinstance(obj.customers_list, dict):
            return sum(
                Decimal(str(customer.get("taken", 0)))
                for customer in obj.customers_list.values() if isinstance(customer, dict)
            )
        return Decimal("0.00")

    def get_total_remainder(self, obj):
        """Calculate total remainder amount from the customers_list."""
        if isinstance(obj.customers_list, dict):
            return sum(
                Decimal(str(customer.get("remainder", 0)))
                for customer in obj.customers_list.values() if isinstance(customer, dict)
            )
        return Decimal("0.00")

    def update(self, instance, validated_data):
        """
        Handle updates to the Services instance and its customers_list.
        Mirrors the logic of RantSerializer.update.
        """
        # Update standard fields
        instance.floor = validated_data.get("floor", instance.floor)
        instance.time = validated_data.get("time", instance.time)
        instance.year = validated_data.get("year", instance.year)
        instance.is_approved = validated_data.get("is_approved", instance.is_approved) # Update overall approval

        customers_data_from_request = validated_data.get("customers_list")

        if customers_data_from_request is not None:
            # Ensure the instance's list is a dict
            if not isinstance(instance.customers_list, dict):
                instance.customers_list = {}

            for customer_id, customer_update_data in customers_data_from_request.items():
                if not isinstance(customer_update_data, dict):
                    continue # Skip invalid entries in the request

                customer_id_str = str(customer_id) # Ensure string key

                # Get existing data for this customer or an empty dict
                existing_customer_data = instance.customers_list.get(customer_id_str, {})

                # --- IMPORTANT: Use the correct field name ('service_fee') ---
                # Get the service fee. Prioritize request, fallback to existing, default to 0.
                new_service = Decimal(str(customer_update_data.get('service', existing_customer_data.get('service', 0))))
                # Get the taken amount. Prioritize request, fallback to existing, default to 0.
                new_taken = Decimal(str(customer_update_data.get('taken', existing_customer_data.get('taken', 0))))
                # Calculate the remainder
                new_remainder = new_service - new_taken
                # Get individual approval status (optional, if you want per-customer approval)
                # Defaults to the instance's overall status if not provided per customer
                new_is_approved = customer_update_data.get('is_approved', instance.is_approved)

                # Prepare the updated data dictionary for this customer
                updated_data_for_customer = {
                    **existing_customer_data, # Start with existing data (preserves 'shop', etc.)
                    "service": float(new_service),
                    "taken": float(new_taken),
                    "remainder": float(new_remainder),
                    "is_approved": new_is_approved, # Update individual approval status
                }

                # Update the customer's data in the instance's list
                instance.customers_list[customer_id_str] = updated_data_for_customer

        # The model's save method will now recalculate 'total' based on the updated list
        instance.save()
        return instance

    