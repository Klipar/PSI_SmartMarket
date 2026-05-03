from .models import Tovar, Sarza
from django.db.models import Sum, F

class InventoryRepository:
    """Class for clean database queries (Read-only operations)"""

    @staticmethod
    def get_items_below_limit():
        """For UC02: Find everything that needs to be reordered"""
        return Tovar.objects.annotate(
            total_qty=Sum('sarze__mnozstvo')
        ).filter(total_qty__lt=F('kriticky_limit'))

    @staticmethod
    def get_sarza_by_ean(ean):
        """Search for batches by product EAN code"""
        return Sarza.objects.filter(tovar__ean_kod=ean).select_related('tovar')