from django.db import transaction, connection
from django.core.management import call_command
from .models import Tovar, Sarza, NavrhObjednavky, Dodavatel

class DBService:
    """
    A central service for database management and high-level ORM operations
    """

    @staticmethod
    def run_migrations():
        """Програмний запуск міграцій (якщо потрібно з коду)"""
        try:
            call_command('migrate', interactive=False)
            return True
        except Exception as e:
            print(f"Migration error: {e}")
            return False

    @staticmethod
    @transaction.atomic
    def init_basic_data():
        """Первинне наповнення БД для тестування юзкейсів"""
        # Створюємо базового постачальника, якщо його немає
        dodavatel, _ = Dodavatel.objects.get_or_create(
            meno="М'ясний Всесвіт",
            defaults={'email': 'contact@meatworld.com'}
        )

        # Створюємо тестовий товар
        tovar, _ = Tovar.objects.get_or_create(
            ean_kod="4820001234567",
            defaults={
                'nazov': 'Ковбаса Дрогобицька',
                'kriticky_limit': 5,
                'dodavatel': dodavatel
            }
        )
        return tovar

    @staticmethod
    def get_db_status():
        """Перевірка зв'язку з SQLite"""
        try:
            connection.ensure_connection()
            return "Connected"
        except Exception:
            return "Disconnected"

    @staticmethod
    @transaction.atomic
    def safe_bulk_update_prices(sarza_ids, discount_percent):
        """
        Приклад 'рихлого' використання ORM:
        Масове оновлення цін для UC03 (Exspirácia)
        """
        multiplier = (100 - discount_percent) / 100
        # Виконуємо одним запитом до БД для продуктивності
        updated_count = Sarza.objects.filter(id__in=sarza_ids).update(
            aktualna_cena=models.F('aktualna_cena') * multiplier
        )
        return updated_count