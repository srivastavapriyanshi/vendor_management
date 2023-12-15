from .views import PurchaseOrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_orders')
urlpatterns = router.urls


