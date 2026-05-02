from django.urls import path
from .views import ReceiveBatchView, SmartReorderView, ExpiringSoonView, InventoryCheckView

urlpatterns = [
    # UC01
    path('stock/receive/', ReceiveBatchView.as_view(), name='receive-batch'),

    # UC02
    path('orders/smart-reorder/', SmartReorderView.as_view(), name='smart-reorder'),

    # UC03
    path('stock/expiring/', ExpiringSoonView.as_view(), name='expiring-soon'),
    path('stock/discount/<int:pk>/', ExpiringSoonView.as_view(), name='apply-discount'),

    path('inventory/start/', InventoryCheckView.as_view(), name='inventory-start'),
    path('inventory/<int:pk>/check/', InventoryCheckView.as_view(), name='inventory-check'),


    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]