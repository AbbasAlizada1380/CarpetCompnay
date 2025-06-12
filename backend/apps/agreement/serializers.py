# import json
# from decimal import Decimal

# from rest_framework import serializers

# from .models import Agreement


# class AgreementSerializer(serializers.ModelSerializer):
#     shop = serializers.ListField(child=serializers.CharField(), required=False)

#     class Meta:
#         model = Agreement
#         fields = [
#             "id",
#             "customer",
#             "status",
#             "shop",
#             "advance",
#             "rant",
#             "service",
#             "floor",
#         ]

#     def create(self, validated_data):

#         shop_data = validated_data.pop("shop", [])

#         # If shop data is passed as a stringified list, fix it
#         if isinstance(shop_data, str):
#             try:
#                 shop_data = json.loads(shop_data)  # Parse the string as JSON
#             except json.JSONDecodeError:
#                 shop_data = []  # Default to an empty list if parsing fails

#         # Create the Agreement and save the shop list
#         agreement = Agreement.objects.create(**validated_data)
#         agreement.set_shop_list(shop_data)
#         agreement.save()
#         return agreement

#     def update(self, instance, validated_data):
#         # Update the fields
#         instance.floor = validated_data.get("floor", instance.floor)
#         instance.time = validated_data.get("time", instance.time)
#         instance.year = validated_data.get("year", instance.year)

#         customers_data = validated_data.get("customers_list", None)
#         if customers_data:
#             for customer_id, customer_data in customers_data.items():
#                 # Ensure 'rant', 'taken', and 'remainder' keys exist in customer data
#                 if str(customer_id) in instance.customers_list:
#                     customer = instance.customers_list[str(customer_id)]

#                     # Safely access keys with default values if missing
#                     customer["taken"] = float(
#                         customer_data.get("taken", customer.get("taken", 0))
#                     )
#                     customer["remainder"] = float(
#                         customer_data.get("remainder", customer.get("remainder", 0))
#                     )
#                     customer["rant"] = float(
#                         customer_data.get("rant", customer.get("rant", 0))
#                     )  # Default to 0 if missing
#                 else:
#                     # If the customer is not in the list, add it with defaults
#                     instance.customers_list[str(customer_id)] = {
#                         "taken": float(customer_data.get("taken", 0)),
#                         "remainder": float(customer_data.get("remainder", 0)),
#                         "rant": float(
#                             customer_data.get("rant", 0)
#                         ),  # Default to 0 if missing
#                     }

#             # Recalculate the total after modifying the customers' data
#             instance.total = sum(
#                 float(
#                     customer.get("rant", 0)
#                 )  # Use .get() to safely handle missing 'rant'
#                 for customer in instance.customers_list.values()
#             )

#         # Save the instance with the updated fields
#         instance.save()
#         return instance

#     def to_representation(self, instance):
#         """
#         Customize the output to ensure numeric fields (Decimal) are returned as floats
#         without quotes.
#         """
#         data = super().to_representation(instance)

#         # Convert Decimal fields to float, and handle None values gracefully
#         data["advance"] = float(data["advance"]) if data["advance"] is not None else 0.0
#         data["rant"] = float(data["rant"]) if data["rant"] is not None else 0.0
#         data["service"] = float(data["service"]) if data["service"] is not None else 0.0

#         return data
# serializers.py
import json
from decimal import Decimal
from rest_framework import serializers
from .models import Agreement


class AgreementSerializer(serializers.ModelSerializer):
    shop = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Agreement
        fields = [
            "id",
            "customer",
            "status",
            "shop",
            "advance",
            "rant",
            "service",
            "floor",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        shop_data = validated_data.pop("shop", [])
        if isinstance(shop_data, str):
            try:
                shop_data = json.loads(shop_data)  
            except json.JSONDecodeError:
                shop_data = [] 

        agreement = Agreement.objects.create(**validated_data)
        agreement.set_shop_list(shop_data)
        agreement.save()
        return agreement

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.advance = validated_data.get("advance", instance.advance)
        instance.rant = validated_data.get("rant", instance.rant)
        instance.service = validated_data.get("service", instance.service)
        instance.floor = validated_data.get("floor", instance.floor)



        shop_data = validated_data.get("shop")
        if shop_data is not None:
            if isinstance(shop_data, str): 
                try:
                    shop_data = json.loads(shop_data)
                except json.JSONDecodeError:
                    shop_data = []  
            instance.set_shop_list(shop_data)

        instance.save() 
        return instance


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["advance"] = float(data["advance"]) if data["advance"] is not None else 0.0
        data["rant"] = float(data["rant"]) if data["rant"] is not None else 0.0
        data["service"] = float(data["service"]) if data["service"] is not None else 0.0

        return data