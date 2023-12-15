from django.shortcuts import render
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from vendors.models import Vendor, VendorPerformance
from vendors.constants import PURCHASE_ORDER_STATUS


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id is not None:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset


    @action(detail=True, methods=['POST'])
    def acknowledge(self, request, pk=None):
        """
        Acknowledge a purchase order and trigger the recalculation of average response time.
        """
        purchase_order = self.get_object()
        if purchase_order.status != PURCHASE_ORDER_STATUS.get("COMPLETED"):
            return Response({'error': 'Purchase order cannot be acknowledged in its current state.'}, status=400)

        if purchase_order.acknowledgment_date:
            return Response({'error': 'Purchase order has already been acknowledged.'}, status=400)
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        vendor = purchase_order.vendor
        vendor_performance, created = VendorPerformance.objects.get_or_create(
            vendor=vendor,
            defaults={
                'on_time_delivery_rate': 0.0,
                'quality_rating': 0.0,
                'average_response_time': 0.0,
                'fulfilment_rate': 0.0,
            }
        )
        acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.order_date).days for po in acknowledged_pos]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        vendor_performance.average_response_time = average_response_time
        vendor_performance.save()
        return Response({'message': 'Purchase order acknowledged successfully.'}, status=200)

