from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Tovar, Sarza, NavrhObjednavky, User, Inventura, ProtokolInventury

class ExpirationService:
    """Service for UC03 (Monitoring and Discounts)"""

    @staticmethod
    def get_expiring_soon(days=2):
        """Find batches expiring within X days"""
        threshold = timezone.now().date() + timedelta(days=days)
        return Sarza.objects.filter(
            datum_exspiracie__lte=threshold,
            mnozstvo__gt=0
        ).select_related('tovar')

    @staticmethod
    @transaction.atomic
    def apply_batch_discount(sarza_id, discount_percent):
        """Apply a discount to a specific batch"""
        sarza = Sarza.objects.get(pk=sarza_id)
        sarza.aplikovat_zlavu(discount_percent)
        return sarza


class InventoryService:
    """Service for UC04 (Digital Inventory)"""
    @staticmethod
    @transaction.atomic
    def start_inventory(user, kategoria):
        """Start inventory (Steps 1-2 of the scenario)"""
        return Inventura.objects.create(vykonal=user, kategoria=kategoria)

    @staticmethod
    @transaction.atomic
    def record_item_check(inventura_id, tovar_id, real_qty):
        """Comparison and registration of discrepancies (Steps 3-7 of the scenario)"""
        tovar = Tovar.objects.get(pk=tovar_id)
        system_qty = tovar.aktualny_stav()
        difference = real_qty - system_qty

        if difference != 0:
            ProtokolInventury.objects.create(
                inventura_id=inventura_id,
                zisteny_rozdiel=difference,
                poznamka=f"Difference for {tovar.nazov}: System {system_qty}, Reality {real_qty}"
            )

        return {
            "tovar": tovar.nazov,
            "system_qty": system_qty,
            "real_qty": real_qty,
            "difference": difference,
            "status": "match" if difference == 0 else "discrepancy"
        }

from django.db.models import F
from .models import Tovar, NavrhObjednavky, PolozkaObjednavky

class OrderService:
    @staticmethod
    def generate_smart_reorder():
        low_stock_items = Tovar.objects.filter(aktualne_mnozstvo__lt=F('min_mnozstvo'))

        supplier_orders = {}
        for tovar in low_stock_items:
            if not tovar.dodavatel:
                continue

            if tovar.dodavatel not in supplier_orders:
                supplier_orders[tovar.dodavatel] = []

            mnozstvo_na_objednanie = (tovar.min_mnozstvo * 2) - tovar.aktualne_mnozstvo

            supplier_orders[tovar.dodavatel].append({
                'tovar': tovar,
                'mnozstvo': mnozstvo_na_objednanie
            })

        created_orders = []
        for supplier, items in supplier_orders.items():
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
    """Service for UC01 (Warehouse Operations)"""

    @staticmethod
    @transaction.atomic
    def receive_new_batch(ean_code, batch_id, quantity, expiration_date, price):
        """UC01: Receiving a new batch of goods"""
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
            raise ValueError(f"Product with EAN {ean_code} does not exist!")