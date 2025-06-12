# apps/services/models.py

from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
# Make sure this import path is correct for your project structure
from apps.agreement.models import Agreement # Assuming Agreement model is here

class Services(models.Model):
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

    floor = models.CharField(_("Floor"), choices=FLOOR_CHOICES, max_length=50)
    time = models.CharField(_("Time"), choices=MONTH_CHOICES, max_length=250)
    year = models.CharField(max_length=255)
    total = models.DecimalField(
        _("Total Service Fee"), max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    is_approved = models.BooleanField(default=False) # Keep this if needed for service-specific logic
    customers_list = models.JSONField(default=dict)
    # --- REMOVED FIELDS ---
    # total_taken = models.DecimalField(...) # Remove - calculate dynamically
    # total_remainder = models.DecimalField(...) # Remove - calculate dynamically
    # --- END REMOVED FIELDS ---
    created_at = models.DateTimeField(auto_now_add=True, editable=False) # Use editable=False like in rent
    updated_at = models.DateTimeField(auto_now=True, editable=False) # Use editable=False like in rent

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['-year', '-time', 'floor'] # Add ordering similar to rent

    def __str__(self):
        # Improve string representation
        return f"Services - Floor {self.get_floor_display()} - {self.get_time_display()} {self.year}"

    def get_initial_customers_data(self):
        """
        Fetches active agreements for the floor and builds the initial customer data list,
        including shop information and initial service fees.
        Mirrors the logic of Rant.get_customers_list.
        """
        if not self.floor:
            return {}, Decimal("0.00")

        try:
            # Ensure Agreement model has a 'service' field or adjust accordingly
            agreements = Agreement.objects.filter(status="Active", floor=self.floor)
        except Exception as e:
            print(f"Error fetching agreements for floor {self.floor} (Services): {e}")
            return {}, Decimal("0.00")

        customers_data = {}
        total_service = Decimal("0.00")

        for agreement in agreements:
            if not agreement.customer:
                continue # Skip agreements without a customer

            # Use agreement.service, default to 0 if None or doesn't exist
            customer_service = getattr(agreement, 'service', None)
            if customer_service is None:
                customer_service = Decimal("0.00")
            else:
                 # Ensure it's a Decimal
                 customer_service = Decimal(str(customer_service))


            taken = Decimal("0.00") # Initially, nothing is taken
            remainder = customer_service - taken

            customer_data = {
                # Use 'service_fee' or similar key to avoid confusion with the model name
                "service": float(customer_service),
                "taken": float(taken),
                "remainder": float(remainder),
                "is_approved": self.is_approved, # Carry over instance approval status
                # Add shop info, similar to rent app
                "shop": str(agreement.shop) if hasattr(agreement, 'shop') and agreement.shop else None,
            }
            customers_data[str(agreement.customer.id)] = customer_data # Use string key
            total_service += customer_service

        return customers_data, total_service

    def save(self, *args, **kwargs):
        """
        On create, populate customers_list and total from initial agreement data.
        On update, recalculate total based on the current customers_list.
        Mirrors the logic of Rant.save.
        """
        is_new = self.pk is None
        if is_new:
            # Populate initial list and total on creation
            customers_data, total_service = self.get_initial_customers_data()
            self.customers_list = customers_data
            self.total = total_service
            # Set initial is_approved status for all customers in the list
            # (Optional: depends if you want initial status tied to instance status)
            for cust_id in self.customers_list:
                if isinstance(self.customers_list[cust_id], dict):
                     self.customers_list[cust_id]['is_approved'] = self.is_approved

        else:
            # Recalculate total based on the potentially updated customers_list
            # Ensure consistency before saving an existing instance
            if isinstance(self.customers_list, dict):
                current_total_service = sum(
                    # Use 'service_fee' key here (or whatever key you used in get_initial_customers_data)
                    Decimal(str(cust_data.get('service', 0)))
                    for cust_data in self.customers_list.values()
                    if isinstance(cust_data, dict)
                )
                self.total = current_total_service

                # Propagate instance's is_approved status to all customers if it changed
                # (Optional: Only if you want a master switch)
                # Check if is_approved is being updated in this save operation
                # This requires checking original value, which isn't straightforward here
                # Simpler: just ensure consistency if needed
                # for cust_id in self.customers_list:
                #    if isinstance(self.customers_list[cust_id], dict):
                #        self.customers_list[cust_id]['is_approved'] = self.is_approved

            else:
                 # Handle cases where customers_list might not be a dict
                 self.customers_list = {} # Reset to empty dict if not valid
                 self.total = Decimal("0.00")

        super().save(*args, **kwargs) # Call the original save method
