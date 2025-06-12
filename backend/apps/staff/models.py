from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # Import timezone for potential default values

class Staff(models.Model):
    """Represents a staff member."""
    class Position(models.TextChoices):
        GARD = "Gard", _("Gard")
        CLEANER = "Cleaner", _("Cleaner")
        ELECTRICAL = "Electrical", _("Electrical")
        MANAGER = "Manager", _("Manager")
        COOKER = "Cooker", _("Cooker")
        FINANCIAL_MANAGER = "FinancialManager", _("Financial Manager") # Choice key clarity

    class Status(models.TextChoices):
        ACTIVE = "Active", _("Active")
        INACTIVE = "Inactive", _("Inactive")

    name = models.CharField(_("Name"), max_length=250)
    father_name = models.CharField(_("Father Name"), max_length=250)
    # Changed NIC to CharField and made optional
    nic = models.CharField(_("NIC"), max_length=50, blank=True, null=True)
    # Made photo optional
    photo = models.ImageField(upload_to="staff/images", blank=True, null=True)
    # Made address optional
    address = models.CharField(_("Address"), max_length=250, blank=True, null=True)
    position = models.CharField(_("Position"), choices=Position.choices, max_length=250)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(_("Status"), choices=Status.choices, max_length=250)

    # --- ADDED/MODIFIED FIELDS ---
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, editable=False) # REMOVED null=True
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, editable=False) # REMOVED null=True
    # --- END ADDED/MODIFIED FIELDS ---

    def __str__(self):
        # Use get_FOO_display() for choice fields for better representation
        return f"{self.name} ({self.get_position_display()})"

    class Meta:
        verbose_name = _("Staff Member")
        verbose_name_plural = _("Staff Members")
        ordering = ['name'] # Add default ordering


class Salary(models.Model):
    """Represents a monthly salary calculation period."""
    MONTH_CHOICES = (
        (1, "حمل"), (2, "ثور"), (3, "جوزا"), (4, "سرطان"),
        (5, "اسد"), (6, "سنبله"), (7, "میزان"), (8, "عقرب"),
        (9, "قوس"), (10, "جدی"), (11, "دلو"), (12, "حوت"),
    )

    month = models.PositiveSmallIntegerField(_("Month"), choices=MONTH_CHOICES)
    year = models.CharField(_("Year"), max_length=4)
    total = models.DecimalField(
        _("Total Salary"), max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    customers_list = models.JSONField(_("Staff Salary Details"), default=dict)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def _get_active_staff_details(self):
        """Helper method to get details for active staff."""
        active_staff = Staff.objects.filter(status=Staff.Status.ACTIVE)
        customers_data = {}
        total_salary = Decimal("0.00")
        for staff in active_staff:
            staff_salary_decimal = staff.salary if staff.salary is not None else Decimal("0.00")
            customer_data = {
                "name": staff.name,
                "salary": str(staff_salary_decimal),
                "taken": "0.00",
                "remainder": str(staff_salary_decimal),
                "description": ""
            }
            customers_data[str(staff.id)] = customer_data # Use string key for JSON
            total_salary += staff_salary_decimal
        return customers_data, total_salary
    def save(self, *args, **kwargs):
        if not self.pk:
            customers_data, total_salary = self._get_active_staff_details()
            self.customers_list = customers_data
            self.total = total_salary
        super().save(*args, **kwargs)

    def __str__(self):
         return f"Salary for {self.get_month_display()} {self.year}"

    class Meta:
        verbose_name = _("Salary Period")
        verbose_name_plural = _("Salary Periods")
        ordering = ['-year', '-month']
        unique_together = ('month', 'year')