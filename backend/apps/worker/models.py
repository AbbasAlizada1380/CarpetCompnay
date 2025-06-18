from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Worker(models.Model):
    name = models.CharField(max_length=300)
    f_name = models.CharField(max_length=300)
    permanent_residency = models.CharField(max_length=300)
    current_residency = models.CharField(max_length=300)
    nic = models.CharField(max_length=300)

    class Meta:
        verbose_name = _("worker")
        verbose_name_plural = _("workers")

    def __str__(self):
        return self.name


class ProcessingCarpet(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    width = models.CharField(max_length=255)
    length = models.CharField(max_length=255)
    map = models.TextField()
    material = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    money = ArrayField(
        models.DecimalField(max_digits=10, decimal_places=2), blank=True, default=list
    )

    def __str__(self):
        return f"{self.width} -- {self.length}"
