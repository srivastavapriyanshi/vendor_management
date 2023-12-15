from rest_framework import serializers
from .models import Vendor, VendorPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'vendor_code', 'name', 'contact_details', 'address')
        read_only_fields = ('vendor_code',)



class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = ('id', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')