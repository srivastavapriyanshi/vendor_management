from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from  vendors.models import Vendor, VendorPerformance
from django.db.models import F
from django.utils import timezone


class PurchaseOrder(models.Model):
    po_number = models.UUIDField(default=uuid.uuid4)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField()
    status = models.IntegerField(default=1, db_index=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.po_number)

