from rest_framework import serializers

from .models import ExportCarpet, ImportCarpet


class ExportCarpetSerializer(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = ExportCarpet
        fields = [
            "id",
            "source",
            "description",
            "first_name",
            "quality",
            "length",
            "width",
            "rate",
            "area",
            "price",
            "weight",
            "created_at",
            "updated_at",
        ]

    def get_area(self, obj):
        return obj.area

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "source": instance.source,
            "description": instance.description,
            "quality": instance.quality,
            "first_name": (
                instance.user.first_name if instance.user else None
            ),  # Accessing username from the related user object
            "length": int(float(instance.length)),
            "width": int(float(instance.width)),
            "rate": int(float(instance.rate)),
            "area": int(instance.area),
            "price": int(float(instance.price)),
            "weight": int(float(instance.weight)),
            "created_at": instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": instance.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ImportCarpetSerializer(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = ImportCarpet
        fields = [
            "id",
            "source",
            "description",
            "first_name",
            "quality",
            "length",
            "width",
            "rate",
            "area",
            "price",
            "weight",
            "created_at",
            "updated_at",
        ]

    def get_area(self, obj):
        return obj.area

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "source": instance.source,
            "description": instance.description,
            "quality": instance.quality,
            "first_name": (
                instance.user.first_name if instance.user else None
            ),  # Accessing username from the related user object
            "length": int(float(instance.length)),
            "width": int(float(instance.width)),
            "rate": int(float(instance.rate)),
            "area": int(instance.area),
            "price": int(float(instance.price)),
            "weight": int(float(instance.weight)),
            "created_at": instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": instance.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
