from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReceiveBatchView, SmartReorderView, ExpiringSoonView,
    InventoryStartView, InventoryRecordView, OrderViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('orders/smart-reorder/', SmartReorderView.as_view(), name='smart_reorder'),
    
    path('', include(router.urls)),
    path('stock/receive/', ReceiveBatchView.as_view(), name='receive_batch'),
    path('stock/expiring/', ExpiringSoonView.as_view(), name='expiring_list'),
    path('stock/expiring/<int:pk>/', ExpiringSoonView.as_view(), name='apply_discount'),
    path('inventory/start/', InventoryStartView.as_view(), name='inventory_start'),
    path('inventory/<int:pk>/check/', InventoryRecordView.as_view(), name='inventory_check'),
]