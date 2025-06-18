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
    material = serializers.ListField(
        child=serializers.CharField(max_length=255), required=False
    )
    money = serializers.ListField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False
    )

    class Meta:
        model = ProcessingCarpet
        fields = ["id", "worker", "width", "length", "map", "material", "money"]
