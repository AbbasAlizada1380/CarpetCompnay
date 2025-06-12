import json
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.customers.models import Customer


class Agreement(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("InActive", "InActive"),
    )

    FLOOR_CHOICES = (
        (1, "First floor"),
        (2, "Second Floor"),
        (3, "Third Floor"),
        (4, "Fourth Floor"),
        (5, "Fifth Floor"),
        (6, "UnderGround"),
    )

    customer = models.ForeignKey(
        Customer, verbose_name="Customer name", on_delete=models.CASCADE
    )
    status = models.CharField("Status", choices=STATUS_CHOICES, max_length=50)

    shop = models.JSONField(blank=True, null=True, default=list)
    advance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal("0.00")
    )
    rant = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal("0.00")
    )
    service = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal("0.00")
    )

    taken = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal("0.00")
    )
    floor = models.CharField(_("Floor"), choices=FLOOR_CHOICES, max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Agreement"
        verbose_name_plural = "Agreements"

    def __str__(self):
        return f"Agreement with {self.customer}"

    def get_shop_list(self):
        return self.shop if self.shop else []

    def set_shop_list(self, shop_list):
        if isinstance(shop_list, list):
            self.shop = shop_list
        else:
            self.shop = []
