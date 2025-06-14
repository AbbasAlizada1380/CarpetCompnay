from django.contrib import admin

from .models import ExportCarpet


class ExportCarpetAdmin(admin.ModelAdmin):
    list_display = ("description", "user", "source", "created_at", "updated_at")

    # Filter carpets by the logged-in user in the admin panel
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all carpets
        return qs.filter(user=request.user)  # Regular users can only see their carpets


admin.site.register(ExportCarpet, ExportCarpetAdmin)
