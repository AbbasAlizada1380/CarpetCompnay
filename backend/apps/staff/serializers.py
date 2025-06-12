import json
from decimal import Decimal, InvalidOperation
from rest_framework import serializers
from .models import Salary, Staff

class StaffSerializer(serializers.ModelSerializer):
    """Serializer for the Staff model."""
    # Explicitly define photo URL field for clarity if needed elsewhere
    photo_url = serializers.ImageField(source='photo', read_only=True, use_url=True)

    class Meta:
        model = Staff
        fields = [
            "id", "name", "father_name", "nic",
            "photo", # Field for uploads
            "photo_url", # Field for retrieving the URL
            "address", "position", "salary", "status",
            # --- ADDED FIELDS ---
            "created_at",
            "updated_at",
        ]
        # --- Make timestamp fields read-only ---
        read_only_fields = ('created_at', 'updated_at', 'photo_url')

    def to_representation(self, instance):
        """Convert Decimal salary to float for JSON, handle timestamps."""
        data = super().to_representation(instance)
        try:
            # Robust conversion of salary to float
            salary_decimal = instance.salary if isinstance(instance.salary, Decimal) else Decimal(str(instance.salary or '0.00'))
            data["salary"] = float(salary_decimal)
        except (ValueError, TypeError, InvalidOperation):
            data["salary"] = 0.0 # Default on error

        # Timestamps are returned in ISO 8601 format by default, which is standard for APIs.
        # No explicit formatting needed here unless a different format is required.
        # Example: data['created_at'] = instance.created_at.strftime("%Y/%m/%d %H:%M")
        return data

class SalarySerializer(serializers.ModelSerializer):
    """Serializer for the Salary model, handling updates and representation."""
    # Add fields for calculated totals shown in the frontend
    total_taken = serializers.FloatField(read_only=True, default=0.0)
    total_remainder = serializers.FloatField(read_only=True, default=0.0)

    class Meta:
        model = Salary
        fields = (
            "id", "month", "year", "total", "customers_list",
            "created_at", "updated_at",
            # Add calculated fields for representation
            "total_taken", "total_remainder",
        )
        # Total is calculated, timestamps are auto-managed
        read_only_fields = ('created_at', 'updated_at', 'total', 'total_taken', 'total_remainder')

    def _parse_decimal(self, value, default=Decimal("0.00")):
        """Safely parse a value to Decimal."""
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return default

    def update(self, instance, validated_data):
        """Handle updates, especially to the nested customers_list."""
        instance.month = validated_data.get("month", instance.month)
        instance.year = validated_data.get("year", instance.year)
        # Get the incoming customers_list data from the request
        incoming_customers_data = validated_data.get("customers_list", None)

        # Ensure the instance's customers_list is a dictionary
        current_customers_list = instance.customers_list
        if not isinstance(current_customers_list, dict):
            try:
                current_customers_list = json.loads(current_customers_list) if isinstance(current_customers_list, str) else {}
            except json.JSONDecodeError:
                current_customers_list = {}
        instance.customers_list = current_customers_list # Assign back parsed/defaulted dict

        # Process updates only if incoming data is provided and is a dictionary
        if isinstance(incoming_customers_data, dict):
            customers_list_changed = False
            new_total_salary = Decimal("0.00") # Recalculate total based on updates

            # Iterate through incoming updates for each staff member
            for staff_id_str, staff_data_in in incoming_customers_data.items():
                 # Ensure staff_id is string and data is dict
                 staff_id_str = str(staff_id_str)
                 if not isinstance(staff_data_in, dict):
                    print(f"Warning: Invalid data format for staff ID {staff_id_str}. Skipping.")
                    continue

                 # Get existing data for this staff member, or default if new
                 existing_staff_data = current_customers_list.get(staff_id_str, {})

                 # Parse incoming values safely
                 salary = self._parse_decimal(staff_data_in.get("salary", existing_staff_data.get("salary")))
                 taken = self._parse_decimal(staff_data_in.get("taken", existing_staff_data.get("taken")))
                 description = str(staff_data_in.get("description", existing_staff_data.get("description", ""))) # Ensure string
                 remainder = salary - taken

                 # Prepare the updated entry, storing monetary values as strings
                 updated_entry = {
                     "name": str(staff_data_in.get("name", existing_staff_data.get("name", ""))), # Update/preserve name
                     "salary": str(salary),
                     "taken": str(taken),
                     "remainder": str(remainder),
                     "description": description,
                 }

                 # Update if changed
                 if current_customers_list.get(staff_id_str) != updated_entry:
                      current_customers_list[staff_id_str] = updated_entry
                      customers_list_changed = True

                 # Add this staff's salary to the recalculated total
                 new_total_salary += salary

            # If any part of the list changed, update the instance total
            if customers_list_changed:
                instance.total = new_total_salary
                # The instance.customers_list (which is current_customers_list) is already updated

        # Save the Salary instance
        instance.save()
        return instance

    def to_representation(self, instance):
        """Calculate and add totals for representation."""
        data = super().to_representation(instance)
        total_taken = Decimal("0.00")
        total_remainder = Decimal("0.00")

        # Get the customers_list (likely already a dict from super call)
        customers_list_repr = data.get("customers_list", {})
        if not isinstance(customers_list_repr, dict): # Safety check
             customers_list_repr = {}

        # Sum taken and remainder amounts safely
        for staff_id, staff_data in customers_list_repr.items():
            if isinstance(staff_data, dict):
                total_taken += self._parse_decimal(staff_data.get("taken"))
                # Recalculate remainder for representation consistency
                salary_repr = self._parse_decimal(staff_data.get("salary"))
                taken_repr = self._parse_decimal(staff_data.get("taken"))
                staff_data['remainder'] = str(salary_repr - taken_repr) # Update remainder string in representation
                total_remainder += (salary_repr - taken_repr)

        # Add calculated totals as floats to the representation
        data["total_taken"] = float(total_taken)
        data["total_remainder"] = float(total_remainder)

        # Ensure the instance total is also a float
        data["total"] = float(self._parse_decimal(instance.total))
        # Ensure customers_list is included as a dictionary
        data["customers_list"] = customers_list_repr

        return data