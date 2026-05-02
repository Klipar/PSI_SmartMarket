from django.urls import path
from .views import (
    ReceiveBatchView, SmartReorderView, ExpiringSoonView, 
    InventoryStartView, InventoryRecordView
)

urlpatterns = [
    path('stock/receive/', ReceiveBatchView.as_view(), name='receive_batch'),
    path('orders/smart-reorder/', SmartReorderView.as_view(), name='smart_reorder'),
    path('stock/expiring/', ExpiringSoonView.as_view(), name='expiring_list'),
    path('stock/expiring/<int:pk>/', ExpiringSoonView.as_view(), name='apply_discount'),
    
    # Інвентаризація: окремий шлях для старту і для запису по ID
    path('inventory/start/', InventoryStartView.as_view(), name='inventory_start'),
    path('inventory/<int:pk>/check/', InventoryRecordView.as_view(), name='inventory_check'),
]