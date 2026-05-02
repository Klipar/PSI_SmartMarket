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