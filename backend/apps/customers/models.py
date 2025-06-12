import os
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    phone_number = models.CharField(_("Phone Number"), max_length=20) 
    rental_owner = models.CharField(max_length=255)
    attachment = models.FileField(
        _("Attachment (Image or Document)"),
        upload_to="media/customer_attachments/",
        blank=True, 
        null=True, 

    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nic = models.CharField(_("NIC"), max_length=50)
    address = models.CharField(_("Address"), max_length=250)

    def __str__(self):
        return f"Customer: {self.name}, Father: {self.father_name}."

    @property
    def attachment_type(self):
        if not self.attachment:
            return None
        try:
            name, extension = os.path.splitext(self.attachment.name)
            extension = extension.lower()
            if extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                return 'image'
            elif extension == '.pdf':
                return 'pdf'
            else:
                return 'file' 
        except Exception:
            return 'file'