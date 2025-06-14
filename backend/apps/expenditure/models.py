# apps/expenditure/models.py
from decimal import Decimal # Ensure Decimal is imported if not already
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Income(models.Model):
    MONTH_CHOICES = (
        (1, "حمل"), (2, "ثور"), (3, "جوزا"), (4, "سرطان"),
        (5, "اسد"), (6, "سنبله"), (7, "میزان"), (8, "عقرب"),
        (9, "قوس"), (10, "جدی"), (11, "دلو"), (12, "حوت"),
    )

    source = models.CharField(max_length=550)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.0")) # Use Decimal for default
    description = models.TextField(blank=True) # Allow blank description
    year = models.CharField(max_length=4) # Limit year length
    month = models.PositiveSmallIntegerField(_("Month"), choices=MONTH_CHOICES) # Use PositiveSmallInt
    receiver = models.CharField(max_length=255)
    # --- ADDED FIELD ---
    consumer = models.CharField(_("Payer/Recorded By"), max_length=255, blank=True, null=True) # Added field, made optional
    # --- END ADDED FIELD ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Income: {self.source} ({self.amount})"

    @classmethod
    def calculate_total_amount(cls):
        total = cls.objects.aggregate(Sum("amount"))
        return total["amount__sum"] if total["amount__sum"] is not None else Decimal("0.0") # Return Decimal

    class Meta:
        ordering = ['-year', '-month', '-created_at'] 