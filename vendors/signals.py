from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import PurchaseOrder
from .models import Vendor, VendorPerformance
from django.db.models import F
from django.db import models
from .constants import PURCHASE_ORDER_STATUS
from django.utils import timezone


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    """
    Signal handler to update vendor performance metrics after a purchase order is saved.
    """
    if instance.vendor:
        vendor = instance.vendor
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating = calculate_quality_rating(vendor)
        average_response_time = calculate_response_time(vendor)
        fulfilment_rate = calculate_fulfilment_rate(vendor)
        vendor_performance = VendorPerformance.objects.create(
            vendor=vendor
        )
        vendor_performance.fulfillment_rate = fulfilment_rate
        vendor_performance.quality_rating_avg = quality_rating
        vendor_performance.on_time_delivery_rate = on_time_delivery_rate
        vendor_performance.average_response_time = average_response_time
        vendor_performance.save()

def calculate_on_time_delivery_rate(vendor):
    total_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status=PURCHASE_ORDER_STATUS.get('COMPLETED'))
    delivered_purchase_orders = total_purchase_orders.filter(delivery_date__lte = models.F('order_date')).count()
    purchase_orders_count = total_purchase_orders.count()
    calculate_on_time_delivery_rate = (delivered_purchase_orders/purchase_orders_count)*100 if purchase_orders_count > 0 else 0.0
    return calculate_on_time_delivery_rate  

def calculate_quality_rating(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status=PURCHASE_ORDER_STATUS.get('COMPLETED'), quality_rating__isnull=False)
    total_quality_ratings = 0.0
    if len(completed_pos) > 0:
        total_quality_ratings =  completed_pos.aggregate(total_quality_ratings=models.Avg('quality_rating'))['total_quality_ratings']
    return total_quality_ratings 

def calculate_response_time(vendor):
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, issue_date__isnull=False, acknowledgment_date__isnull=False)
    diff_days = [(po.acknowledgment_date - po.order_date).days for po in purchase_orders]
    response_time = sum(diff_days) / len(diff_days) if diff_days else 0.0
    return response_time

def calculate_fulfilment_rate(vendor):
    fulfilled_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status = PURCHASE_ORDER_STATUS.get('COMPLETED'), issue_date__isnull=True).count()
    total_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilment_rate = (fulfilled_purchase_orders / total_purchase_orders) * 100 if total_purchase_orders > 0 else 0.0
    return fulfilment_rate 