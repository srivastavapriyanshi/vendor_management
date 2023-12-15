from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.UUIDField(default=uuid.uuid4, db_index=True)

    def __str__(self):
        return self.name


class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor.name}- {self.date.date()} {self.date.time()}"
