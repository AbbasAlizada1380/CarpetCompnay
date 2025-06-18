from rest_framework import serializers

from .models import ProcessingCarpet, Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            "id",
            "name",
            "f_name",
            "permanent_residency",
            "current_residency",
            "nic",
        ]


class ProcessingCarpetSerializer(serializers.ModelSerializer):
    worker = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all())
    material = serializers.ListField(
        child=serializers.CharField(max_length=255), required=False
    )
    money = serializers.ListField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False
    )

    class Meta:
        model = ProcessingCarpet
        fields = ["id", "worker", "width", "length", "map", "material", "money"]

    def create(self, validated_data):
        # Convert Decimal values to strings
        if "money" in validated_data:
            validated_data["money"] = [str(m) for m in validated_data["money"]]

        # Create the ProcessingCarpet instance
        processing_carpet = ProcessingCarpet.objects.create(**validated_data)
        return processing_carpet

    def update(self, instance, validated_data):
        if "money" in validated_data:
            validated_data["money"] = [str(m) for m in validated_data["money"]]
        return super().update(instance, validated_data)
