# apps/units/serializers.py
import json
from decimal import Decimal, InvalidOperation

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Finance, Unit, UnitBill


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for the Unit model."""

    class Meta:
        model = Unit
        fields = [
            "id",
            "customer_name",
            "customer_father_name",
            "unit_number",
            "services_description",
            "service_charge",
            "current_water_reading",
            "current_electricity_reading",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        status = data.get("status", self.instance.status if self.instance else None)
        customer_name = data.get(
            "customer_name", self.instance.customer_name if self.instance else None
        )

        if status == Unit.Status.OCCUPIED and not customer_name:
            raise serializers.ValidationError(
                {
                    "customer_name": _(
                        "Occupier Name is required when status is Occupied."
                    )
                }
            )

        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["service_charge"] = float(instance.service_charge or 0.0)
        data["current_water_reading"] = float(instance.current_water_reading or 0.0)
        data["current_electricity_reading"] = float(
            instance.current_electricity_reading or 0.0
        )
        return data


class UnitBillSerializer(serializers.ModelSerializer):
    total_paid = serializers.FloatField(read_only=True, default=0.0)
    total_remainder = serializers.FloatField(read_only=True, default=0.0)
    unit_details_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UnitBill
        fields = (
            "id",
            "month",
            "year",
            "total",
            "unit_details_list",
            "created_at",
            "updated_at",
            "total_paid",
            "total_remainder",
        )

    def _parse_decimal(self, value, default=Decimal("0.00")):
        try:
            if value is None or str(value).strip() == "":
                return default
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return default

    def get_unit_details_list(self, instance):
        output_list = {}
        details = instance.unit_details_list
        if not isinstance(details, dict):
            try:
                details = json.loads(details)
            except (TypeError, json.JSONDecodeError):
                return {}

        for unit_id_str, data in details.items():
            if not isinstance(data, dict):
                continue

            charge = self._parse_decimal(data.get("service_charge"))
            paid = self._parse_decimal(data.get("amount_paid"))
            current_water = self._parse_decimal(data.get("current_water_reading"))
            previous_water = self._parse_decimal(
                data.get("previous_water_reading", current_water)
            )
            current_elec = self._parse_decimal(data.get("current_electricity_reading"))
            previous_elec = self._parse_decimal(
                data.get("previous_electricity_reading", current_elec)
            )

            # Use stored values only (no calculation)
            total_water_price = self._parse_decimal(
                data.get("total_water_price", "0.0")
            )
            total_electricity = self._parse_decimal(
                data.get("total_electricity", "0.0")
            )

            totals = charge + total_water_price + total_electricity

            taken = self._parse_decimal(data.get("taken", "0.0"))
            remainder = totals - taken

            output_data = {
                "unit_id": data.get("unit_id"),
                "customer_name": data.get("customer_name"),
                "customer_father_name": data.get("customer_father_name"),
                "unit_number": data.get("unit_number"),
                "services": float(charge),
                "service_description_text": data.get("services_description"),
                "description": data.get("description", ""),
                "previous_waterMeter": float(previous_water),
                "current_waterMeter": float(current_water),
                "previous_electricityMeter": float(previous_elec),
                "current_electricityMeter": float(current_elec),
                "total_water_price": float(total_water_price),
                "total_electricity": float(total_electricity),
                "remainder": float(remainder),
                "taken": float(taken),
                "totals": float(totals),
            }

            output_list[unit_id_str] = output_data

        return output_list

    def update(self, instance, validated_data):
        instance.month = validated_data.get("month", instance.month)
        instance.year = validated_data.get("year", instance.year)
        request_data = self.context["request"].data
        incoming_unit_data = request_data.get("unit_details_list", None)

        current_unit_details = instance.unit_details_list
        if not isinstance(current_unit_details, dict):
            try:
                current_unit_details = (
                    json.loads(current_unit_details)
                    if isinstance(current_unit_details, str)
                    else {}
                )
            except json.JSONDecodeError:
                current_unit_details = {}

        if isinstance(incoming_unit_data, dict):
            details_list_changed = False

            for unit_id_str, unit_data_in in incoming_unit_data.items():
                unit_id_str = str(unit_id_str)
                if not isinstance(unit_data_in, dict):
                    continue

                existing_unit_data = current_unit_details.get(unit_id_str)
                if existing_unit_data is None:
                    print(f"Warning: Unit ID {unit_id_str} not found.")
                    continue

                unit_updated = False

                def get_field(data, *keys):
                    for key in keys:
                        if key in data:
                            return data[key]
                    return None

                new_charge_str = get_field(unit_data_in, "service_charge")
                if new_charge_str is not None:
                    new_charge = self._parse_decimal(new_charge_str)
                    if new_charge != self._parse_decimal(
                        existing_unit_data.get("service_charge")
                    ):
                        existing_unit_data["service_charge"] = str(new_charge)
                        unit_updated = True
                new_water_price_str = get_field(unit_data_in, "total_water_price")
                if new_water_price_str is not None:
                    new_water_price = self._parse_decimal(new_water_price_str)
                    if new_water_price != self._parse_decimal(
                        existing_unit_data.get("total_water_price", "0.0")
                    ):
                        existing_unit_data["total_water_price"] = str(new_water_price)
                        unit_updated = True

                new_electricity_price_str = get_field(unit_data_in, "total_electricity")
                if new_electricity_price_str is not None:
                    new_electricity_price = self._parse_decimal(
                        new_electricity_price_str
                    )
                    if new_electricity_price != self._parse_decimal(
                        existing_unit_data.get("total_electricity", "0.0")
                    ):
                        existing_unit_data["total_electricity"] = str(
                            new_electricity_price
                        )
                        unit_updated = True

                new_taken_str = get_field(unit_data_in, "taken")
                if new_taken_str is not None:
                    new_taken = self._parse_decimal(new_taken_str)
                    if new_taken != self._parse_decimal(
                        existing_unit_data.get("taken")
                    ):
                        existing_unit_data["taken"] = str(new_taken)
                        unit_updated = True

                new_prev_water = get_field(
                    unit_data_in, "previous_water_reading", "previous_waterMeter"
                )
                if new_prev_water is not None:
                    if str(new_prev_water) != existing_unit_data.get(
                        "previous_water_reading"
                    ):
                        existing_unit_data["previous_water_reading"] = str(
                            new_prev_water
                        )
                        unit_updated = True

                new_curr_water = get_field(
                    unit_data_in, "current_water_reading", "current_waterMeter"
                )
                if new_curr_water is not None:
                    if str(new_curr_water) != existing_unit_data.get(
                        "current_water_reading"
                    ):
                        existing_unit_data["current_water_reading"] = str(
                            new_curr_water
                        )
                        unit_updated = True

                new_prev_elec = get_field(
                    unit_data_in,
                    "previous_electricity_reading",
                    "previous_electricityMeter",
                )
                if new_prev_elec is not None:
                    if str(new_prev_elec) != existing_unit_data.get(
                        "previous_electricity_reading"
                    ):
                        existing_unit_data["previous_electricity_reading"] = str(
                            new_prev_elec
                        )
                        unit_updated = True

                new_curr_elec = get_field(
                    unit_data_in,
                    "current_electricity_reading",
                    "current_electricityMeter",
                )
                if new_curr_elec is not None:
                    if str(new_curr_elec) != existing_unit_data.get(
                        "current_electricity_reading"
                    ):
                        existing_unit_data["current_electricity_reading"] = str(
                            new_curr_elec
                        )
                        unit_updated = True

                # ✅ NEW: Update description
                new_description = get_field(unit_data_in, "description")
                if new_description is not None:
                    if new_description != existing_unit_data.get("description", ""):
                        existing_unit_data["description"] = str(new_description)
                        unit_updated = True

                if unit_updated:
                    service_charge = self._parse_decimal(
                        existing_unit_data.get("service_charge", "0.0")
                    )
                    water_price = self._parse_decimal(
                        existing_unit_data.get("total_water_price", "0.0")
                    )
                    elec_price = self._parse_decimal(
                        existing_unit_data.get("total_electricity", "0.0")
                    )
                    amount_paid = self._parse_decimal(
                        existing_unit_data.get("taken", "0.0")
                    )

                    totals = service_charge + water_price + elec_price
                    remainder = totals - amount_paid

                    existing_unit_data["totals"] = str(totals)
                    existing_unit_data["remainder"] = str(remainder)

                    details_list_changed = True

                    unit_obj = Unit.objects.filter(id=int(unit_id_str)).first()
                    if unit_obj:
                        if new_curr_water is not None:
                            unit_obj.current_water_reading = self._parse_decimal(
                                new_curr_water
                            )
                        if new_curr_elec is not None:
                            unit_obj.current_electricity_reading = self._parse_decimal(
                                new_curr_elec
                            )
                        unit_obj.save()

            if details_list_changed:
                instance.unit_details_list = json.dumps(current_unit_details)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        total_charge = Decimal("0.00")
        total_paid_calc = Decimal("0.00")
        total_remainder_calc = Decimal("0.00")

        unit_details_repr = data.get("unit_details_list", {})

        if not isinstance(unit_details_repr, dict):
            unit_details_repr = {}

        # Loop through each unit detail
        for unit_id, unit_data in unit_details_repr.items():
            if isinstance(unit_data, dict):
                # Add up totals, paid, and remainder
                total_charge += self._parse_decimal(unit_data.get("totals", "0.0"))
                total_paid_calc += self._parse_decimal(unit_data.get("taken", "0.0"))
                total_remainder_calc += self._parse_decimal(
                    unit_data.get("remainder", "0.0")
                )

        # Set the final calculated fields
        data["total"] = float(total_charge)
        data["total_paid"] = float(total_paid_calc)
        data["total_remainder"] = float(total_remainder_calc)

        return data


class FinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Finance
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Convert amount to integer if it exists
        amount = data.get("amount")
        if amount is not None:
            data["amount"] = int(float(amount))  # handles Decimal, float, string, etc.

        return data
