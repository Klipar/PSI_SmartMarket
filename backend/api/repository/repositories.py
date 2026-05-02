from .models import Tovar, Sarza
from django.db.models import Sum, F

class InventoryRepository:
    """Клас для чистих запитів до БД (Read-only operations)"""

    @staticmethod
    def get_items_below_limit():
        """Для UC02: Знайти все, що треба дозамовити"""
        return Tovar.objects.annotate(
            total_qty=Sum('sarze__mnozstvo')
        ).filter(total_qty__lt=F('kriticky_limit'))

    @staticmethod
    def get_sarza_by_ean(ean):
        """Пошук партій за EAN кодом товару"""
        return Sarza.objects.filter(tovar__ean_kod=ean).select_related('tovar')