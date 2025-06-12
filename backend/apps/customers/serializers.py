
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    
    attachment = serializers.FileField(
        use_url=True,
        required=False,
        allow_null=True,
        allow_empty_file=True 
    )

   

    attachment_type = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "father_name",
            "phone_number",
            "attachment",     
            "attachment_type",  
            "rental_owner",
            "nic",
            "address",
            "created_at",
            "updated_at",
        ]
    