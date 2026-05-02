class ExpirationService:
    """Сервіс для UC03 (Моніторинг та знижки)"""

    @staticmethod
    def get_expiring_soon(days=2):
        """Знайти партії, що виходять з ладу через X днів"""
        threshold = timezone.now().date() + timedelta(days=days)
        return Sarza.objects.filter(
            datum_exspiracie__lte=threshold,
            mnozstvo__gt=0
        ).select_related('tovar')

    @staticmethod
    @transaction.atomic
    def apply_batch_discount(sarza_id, discount_percent):
        """Застосувати знижку до конкретної партії"""
        sarza = Sarza.objects.get(pk=sarza_id)
        sarza.aplikovat_zlavu(discount_percent)
        return sarza


class InventoryService:
    @staticmethod
    @transaction.atomic
    def start_inventory(user, kategoria):
        """Початок інвентаризації (Крок 1-2 сценарію)"""
        return Inventura.objects.create(vykonal=user, kategoria=kategoria)

    @staticmethod
    @transaction.atomic
    def record_item_check(inventura_id, tovar_id, real_qty):
        """Порівняння та реєстрація розбіжностей (Крок 3-7 сценарію)"""
        tovar = Tovar.objects.get(pk=tovar_id)
        system_qty = tovar.aktualny_stav()
        difference = real_qty - system_qty
        
        # Створюємо протокол, якщо є розбіжність (UC04: 6-7)
        if difference != 0:
            ProtokolInventury.objects.create(
                inventura_id=inventura_id,
                zisteny_rozdiel=difference,
                poznamka=f"Rozdiel pre {tovar.nazov}: Systém {system_qty}, Realita {real_qty}"
            )
        
        return {
            "tovar": tovar.nazov,
            "system_qty": system_qty,
            "real_qty": real_qty,
            "difference": difference,
            "status": "match" if difference == 0 else "discrepancy"
        }

class OrderService:
    """Сервіс для UC02 (Smart-Reorder)"""

    @staticmethod
    @transaction.atomic
    def generate_smart_reorder():
        """UC02: Автоматичне створення замовлень для товарів нижче ліміту"""
        from .repositories import InventoryRepository

        low_stock_items = InventoryRepository.get_items_below_limit()
        created_orders = []

        # Групуємо по постачальнику
        suppliers_map = {}
        for tovar in low_stock_items:
            if tovar.dodavatel:
                suppliers_map.setdefault(tovar.dodavatel, []).append(tovar)

        for supplier, items in suppliers_map.items():
            # Створюємо замовлення в статусі "На схвалення"
            order = NavrhObjednavky.objects.create(
                dodavatel=supplier,
                stav=NavrhObjednavky.Status.NA_SCHVALENIE
            )

            # Додаємо позиції (наприклад, замовляємо критичний ліміт * 2)
            for item in items:
                order.polozky.create(
                    tovar=item,
                    mnozstvo=item.kriticky_limit * 2,
                    cena_pri_objednavke=0 # Буде уточнено менеджером
                )
            created_orders.append(order)

        return created_orders

from django.db import transaction
from .models import Tovar, Sarza, NavrhObjednavky, User
from django.utils import timezone
from datetime import timedelta

class StockService:
    """Сервіс для UC01 та UC04 (Складські операції)"""

    @staticmethod
    @transaction.atomic
    def receive_new_batch(ean_code, batch_id, quantity, expiration_date, price):
        """UC01: Прийом нової партії товару"""
        try:
            tovar = Tovar.objects.get(ean_kod=ean_code)
            new_sarza = Sarza.objects.create(
                tovar=tovar,
                id_sarze=batch_id,
                mnozstvo=quantity,
                datum_exspiracie=expiration_date,
                aktualna_cena=price
            )
            return new_sarza
        except Tovar.DoesNotExist:
            raise ValueError(f"Tovar s EAN {ean_code} neexistuje!")