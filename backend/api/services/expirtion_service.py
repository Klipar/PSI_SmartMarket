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