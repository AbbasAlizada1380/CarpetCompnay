# apps/rent/models.py

from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
# Make sure this import path is correct for your project structure
from apps.agreement.models import Agreement

class Rant(models.Model):
    FLOOR_CHOICES = (
        (1, "First floor"),
        (2, "Second Floor"),
        (3, "Third Floor"),
        (4, "Fourth Floor"),
        (5, "Fifth Floor"),
        (6, "UnderGround"),
    )

    MONTH_CHOICES = (
        (1, "حمل"), (2, "ثور"), (3, "جوزا"), (4, "سرطان"),
        (5, "اسد"), (6, "سنبله"), (7, "میزان"), (8, "عقرب"),
        (9, "قوس"), (10, "جدی"), (11, "دلو"), (12, "حوت"),
    )

    year = models.CharField(max_length=255)
    floor = models.CharField(_("Floor"), choices=FLOOR_CHOICES, max_length=50)
    time = models.CharField(_("Time"), choices=MONTH_CHOICES, max_length=250)
    total = models.DecimalField(
        _("Total"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    customers_list = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Rant")
        verbose_name_plural = _("Rants")
        ordering = ['-year', '-time', 'floor']

    def __str__(self):
        return f"Rent - Floor {self.get_floor_display()} - {self.get_time_display()} {self.year}"

    def get_customers_list(self):
        """
        Fetches active agreements for the floor and builds the initial customer data list,
        including shop information.
        """
        # Ensure 'floor' has a value before querying
        if not self.floor:
             return {}, Decimal("0.00") # Return empty if floor is not set

        try:
            agreements = Agreement.objects.filter(status="Active", floor=self.floor)
        except Exception as e:
            # Handle potential errors during query, e.g., log the error
            print(f"Error fetching agreements for floor {self.floor}: {e}")
            return {}, Decimal("0.00")

        customers_data = {}
        total_rent = Decimal("0.00")

        for agreement in agreements:
            # Ensure agreement has a customer associated
            if not agreement.customer:
                continue # Skip agreements without a customer

            taken = Decimal("0.00")
            customer_rant = agreement.rant if agreement.rant is not None else Decimal("0.00")
            remainder = customer_rant - taken

            # Prepare customer data dictionary
            customer_data = {
                "rant": float(customer_rant),
                "taken": float(taken),
                "remainder": float(remainder),
                # --- ADDED LINE: Include shop info ---
                # Using str() for broad compatibility. Adjust if agreement.shop is a ForeignKey
                # e.g., use agreement.shop.number or agreement.shop.name if needed.
                # Add a check if the 'shop' attribute might be missing/None
                "shop": str(agreement.shop) if hasattr(agreement, 'shop') and agreement.shop else None,
            }
            # Use customer ID as the key
            customers_data[str(agreement.customer.id)] = customer_data # Ensure key is string
            total_rent += customer_rant

        return customers_data, total_rent

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            customers_data, total_rent = self.get_customers_list()
            self.customers_list = customers_data
            self.total = total_rent
        else:
            # Recalculate total based on the potentially updated customers_list
            # Ensure consistency before saving an existing instance
            if isinstance(self.customers_list, dict):
                current_total_rant = sum(
                    Decimal(str(cust_data.get('rant', 0)))
                    for cust_data in self.customers_list.values()
                    if isinstance(cust_data, dict)
                )
                self.total = current_total_rant
            else:
                 # Handle cases where customers_list might not be a dict (e.g., corrupted data)
                 self.customers_list = {} # Reset to empty dict if not valid
                 self.total = Decimal("0.00")


        super().save(*args, **kwargs)