from rest_framework import generics
from .serializers import VendorSerializer, VendorPerformanceSerializer
from .models import Vendor, VendorPerformance
from orders.models import PurchaseOrder
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import models
from .constants import PURCHASE_ORDER_STATUS


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        """
        Retrieve a vendor's performance metrics.
        """
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor_performance = VendorPerformance.objects.filter(vendor = vendor)
        serializer = VendorPerformanceSerializer(vendor_performance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
