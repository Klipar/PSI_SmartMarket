from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Tovar, Sarza, NavrhObjednavky, User, Inventura, ProtokolInventury

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
    """Сервіс для UC04 (Цифрова інвентаризація)"""
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

from django.db.models import F
from .models import Tovar, NavrhObjednavky, PolozkaObjednavky # Додай PolozkaObjednavky якщо є

class OrderService:
    @staticmethod
    def generate_smart_reorder():
        # Шукаємо товари, де кількість менша за мінімальний ліміт
        # (Припускаємо, що в моделі Tovar є поля: aktualne_mnozstvo, min_mnozstvo, dodavatel)
        low_stock_items = Tovar.objects.filter(aktualne_mnozstvo__lt=F('min_mnozstvo'))

        # 3.1 Zlúčenie objednávok: Групуємо за постачальником
        supplier_orders = {}
        for tovar in low_stock_items:
            if not tovar.dodavatel:
                # Виняток: Nedostupný dodávateľ
                continue

            if tovar.dodavatel not in supplier_orders:
                supplier_orders[tovar.dodavatel] = []

            # Розрахунок кількості: наприклад, замовляємо стільки, щоб покрити 2x мінімум
            mnozstvo_na_objednanie = (tovar.min_mnozstvo * 2) - tovar.aktualne_mnozstvo

            supplier_orders[tovar.dodavatel].append({
                'tovar': tovar,
                'mnozstvo': mnozstvo_na_objednanie
            })

        created_orders = []
        for supplier, items in supplier_orders.items():
            # Створюємо драфт замовлення (Výstupné podmienky: stav „Na schválenie“)
            order = NavrhObjednavky.objects.create(
                dodavatel=supplier,
                stav='Pending Approval'
            )

            for item_data in items:
                PolozkaObjednavky.objects.create(
                    objednavka=order,
                    tovar=item_data['tovar'],
                    navrhovane_mnozstvo=item_data['mnozstvo'],
                    cena_za_kus=item_data['tovar'].aktualna_cena
                )
            created_orders.append(order)

        return created_orders

class StockService:
    """Сервіс для UC01 (Складські операції)"""

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