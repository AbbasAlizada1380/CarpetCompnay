# apps/units/admin.py
from django.contrib import admin
from .models import Unit, UnitBill

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_number',
        'customer_name', # Use direct field
        'customer_father_name', # Use direct field
        'status',
        'service_charge', # Display service charge
        'current_water_reading',
        'current_electricity_reading',
        'updated_at'
    )
    list_filter = ('status',)
    search_fields = ('unit_number', 'customer_name', 'customer_father_name') 
    list_editable = ('status', 'customer_name', 'customer_father_name', 'service_charge') # Allow editing direct fields
    list_display_links = ('unit_number',)

    fieldsets = (
        (None, {
            'fields': ('unit_number', 'status', 'services_description')
        }),
        ('Occupier Details', { # Group occupier info
            'fields': ('customer_name', 'customer_father_name')
        }),
        ('Billing & Meter Readings', { # Group billing/meter info
             'fields': (
                 'service_charge',
                 'current_water_reading',
                 'current_electricity_reading'
             ),
             'classes': ('collapse',) # Optional: collapse section
        }),
    )

@admin.register(UnitBill)
class UnitBillAdmin(admin.ModelAdmin):
    # ADDED total back
    list_display = ('year', 'get_month_display', 'total', 'created_at')
    list_filter = ('year', 'month')
    readonly_fields = ('unit_details_list', 'total', 'created_at', 'updated_at')
    add_fieldsets = ((None, {'fields': ('month', 'year')}),) # Can only set month/year on add
    fieldsets = (
        (None, {'fields': ('year', 'month')}),
        ('Billing Details (Generated Snapshot)', {
            'fields': ('total', 'unit_details_list', 'created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # Viewing existing object
            return self.readonly_fields + ('month', 'year')
        else: # Adding new object
            return ('total', 'unit_details_list', 'created_at', 'updated_at')
    # ---

    def get_fieldsets(self, request, obj=None):
        if not obj: # Adding
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)