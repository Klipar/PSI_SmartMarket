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