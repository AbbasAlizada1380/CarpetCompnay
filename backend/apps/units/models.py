# apps/units/models.py
from decimal import Decimal, InvalidOperation

from django.db import models
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):
    """Represents a physical unit/shop, storing occupier details directly."""

    class Status(models.TextChoices):
        OCCUPIED = "Occupied", _("Occupied")
        VACANT = "Vacant", _("Vacant")
        MAINTENANCE = "Maintenance", _("Maintenance")

    customer_name = models.CharField(
        _("Occupier Name"), max_length=250, blank=True, null=True
    )
    customer_father_name = models.CharField(
        _("Occupier Father's Name"), max_length=250, blank=True, null=True
    )
    unit_number = models.CharField(_("Unit Number"), max_length=100)
    services_description = models.TextField(
        _("Services Description"), blank=True, null=True
    )
    service_charge = models.DecimalField(
        _("Default Service Charge"),
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    current_water_reading = models.DecimalField(
        _("Current Water Meter Reading"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=Decimal("0.00"),
    )
    current_electricity_reading = models.DecimalField(
        _("Current Electricity Meter Reading"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=Decimal("0.00"),
    )
    # current_electricity_reading= models.DecimalField()
    status = models.CharField(
        _("Status"), choices=Status.choices, max_length=50, default=Status.VACANT
    )

    created_at = models.DateTimeField(
        _("Created At"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, editable=False)

    def __str__(self):
        occupier = self.customer_name if self.customer_name else "No Occupier"
        return f"Unit {self.unit_number} ({occupier})"

    def save(self, *args, **kwargs):
        """Ensure vacant units don't retain occupier details."""
        if self.status == self.Status.VACANT:
            self.customer_name = None
            self.customer_father_name = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ["unit_number"]


class UnitBill(models.Model):
    """Represents a monthly billing period for units."""

    MONTH_CHOICES = (
        (1, "حمل"),
        (2, "ثور"),
        (3, "جوزا"),
        (4, "سرطان"),
        (5, "اسد"),
        (6, "سنبله"),
        (7, "میزان"),
        (8, "عقرب"),
        (9, "قوس"),
        (10, "جدی"),
        (11, "دلو"),
        (12, "حوت"),
    )

    month = models.PositiveSmallIntegerField(_("Month"), choices=MONTH_CHOICES)
    year = models.CharField(_("Year"), max_length=4)
    total = models.DecimalField(
        _("Total Billed Service Charges"),
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    unit_details_list = models.JSONField(_("Unit Bill Details Snapshot"), default=dict)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def _get_billable_unit_details(self):
        """Helper method to get details for OCCUPIED units for snapshot creation."""
        billable_units = Unit.objects.filter(status=Unit.Status.OCCUPIED)
        details_data = {}
        grand_total = Decimal("0.00")
        for unit in billable_units:
            charge = (
                unit.service_charge
                if unit.service_charge is not None
                else Decimal("0.00")
            )
            unit_data = {
                "unit_id": unit.id,
                "customer_name": unit.customer_name or "N/A",
                "customer_father_name": unit.customer_father_name or "",
                "unit_number": unit.unit_number,
                "services_description": unit.services_description or "",
                "service_charge": str(charge),
                "current_water_reading": str(unit.current_water_reading or "0.00"),
                "current_electricity_reading": str(
                    unit.current_electricity_reading or "0.00"
                ),
                "amount_paid": "0.00",
                "remainder": str(charge),
                "description": "",
            }
            details_data[str(unit.id)] = unit_data
            grand_total += charge

        return details_data, grand_total

    def save(self, *args, **kwargs):
        """Generate snapshot and total only on creation."""
        if not self.pk:  # Only on initial creation
            details_data, grand_total = self._get_billable_unit_details()
            self.unit_details_list = details_data
            self.total = grand_total
        # Total recalculation on update is handled in the serializer or explicitly called
        super().save(*args, **kwargs)

    def _parse_decimal(self, value, default=Decimal("0.00")):
        """Safely parse a value to Decimal."""
        try:
            if value is None or str(value).strip() == "":
                return default
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return default

    def recalculate_total_from_details(self):
        """Recalculates the 'total' field based on 'service_charge' in unit_details_list."""
        current_details = self.unit_details_list
        if not isinstance(current_details, dict):
            self.total = Decimal("0.00")  # Reset if details invalid
            return

        new_total = Decimal("0.00")
        for unit_id, data in current_details.items():
            if isinstance(data, dict):
                service_charge = self._parse_decimal(data.get("service_charge"))
                new_total += service_charge
        self.total = new_total

    def __str__(self):
        return f"Unit Bills for {self.get_month_display()} {self.year}"

    class Meta:
        verbose_name = _("Unit Bill Period")
        verbose_name_plural = _("Unit Bill Periods")
        ordering = ["-year", "-month"]
        unique_together = ("month", "year")


class Finance(models.Model):
    form_person = models.CharField(max_length=255)
    to_person = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    issue_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Finance")
        verbose_name_plural = _("Finances")

    def __str__(self):
        return f"From {self.form_person} to {self.to_person}."
