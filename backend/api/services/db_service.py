from django.db import transaction, connection
from django.core.management import call_command
from api.models import Tovar, Sarza, NavrhObjednavky, Dodavatel

class DBService:
    """
    A central service for database management and high-level ORM operations
    """

    @staticmethod
    def run_migrations():
        """Programmatic triggering of migrations (if needed from code)"""
        try:
            call_command('migrate', interactive=False)
            return True
        except Exception as e:
            print(f"Migration error: {e}")
            return False

    @staticmethod
    @transaction.atomic
    def init_basic_data():
        """Initial database populating for use case testing"""
        dodavatel, _ = Dodavatel.objects.get_or_create(
            meno="The Meat Universe",
            defaults={'email': 'contact@meatworld.com'}
        )

        tovar, _ = Tovar.objects.get_or_create(
            ean_kod="4820001234567",
            defaults={
                'nazov': 'Drohobych Sausage',
                'kriticky_limit': 5,
                'dodavatel': dodavatel
            }
        )
        return tovar

    @staticmethod
    def get_db_status():
        """Checking the connection to SQLite"""
        try:
            connection.ensure_connection()
            return "Connected"
        except Exception:
            return "Disconnected"

    @staticmethod
    @transaction.atomic
    def safe_bulk_update_prices(sarza_ids, discount_percent):
        multiplier = (100 - discount_percent) / 100
        updated_count = Sarza.objects.filter(id__in=sarza_ids).update(
            aktualna_cena=models.F('aktualna_cena') * multiplier
        )
        return updated_count