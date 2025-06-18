from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ExportCarpet(models.Model):
    source = models.CharField(max_length=255)
    description = models.TextField()
    quality = models.CharField(max_length=300)
    length = models.DecimalField(decimal_places=2, max_digits=10)
    width = models.DecimalField(decimal_places=2, max_digits=10)
    rate = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    weight = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carpets")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def area(self):
        return self.length * self.width

    def save(self, *args, **kwargs):
        self.price = self.area * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description[:40]


class ImportCarpet(models.Model):
    source = models.CharField(max_length=255)
    description = models.TextField()
    quality = models.CharField(max_length=300)
    length = models.DecimalField(decimal_places=2, max_digits=10)
    width = models.DecimalField(decimal_places=2, max_digits=10)
    rate = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    weight = models.CharField(max_length=255)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="import_carpet"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def area(self):
        return self.length * self.width

    def save(self, *args, **kwargs):
        self.price = self.area * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description[:40]
