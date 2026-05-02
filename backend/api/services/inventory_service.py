class InventoryService:
    """Сервіс для UC04 (Інвентаризація)"""

    @staticmethod
    @transaction.atomic
    def perform_inventory_check(user, tovar_id, real_quantity):
        """Порівняння залишку та створення протоколу розбіжностей"""
        tovar = Tovar.objects.get(pk=tovar_id)
        system_quantity = tovar.aktualny_stav()
        diff = real_quantity - system_quantity

        if diff != 0:
            pass
        return diff