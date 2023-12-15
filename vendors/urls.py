from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDeleteView, VendorPerformanceAPIView

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),

]