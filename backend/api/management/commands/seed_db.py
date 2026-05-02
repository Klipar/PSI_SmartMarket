from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Dodavatel, Tovar, Sarza, NavrhObjednavky
from django.utils import timezone
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Заповнює базу даних початковими даними'

    def handle(self, *args, **kwargs):
        self.stdout.write("Початок сідингу...")

        # 1. Створюємо користувачів різних ролей
        skladnik, _ = User.objects.get_or_create(
            username='ivan_sklad',
            defaults={'role': 'SK', 'first_name': 'Іван', 'usek': 'Сектор А'}
        )
        skladnik.set_password('password123')
        skladnik.save()

        manager, _ = User.objects.get_or_create(
            username='olena_man',
            defaults={'role': 'MN', 'first_name': 'Олена'}
        )
        manager.set_password('password123')
        manager.save()

        # 2. Постачальники
        dodavatel, _ = Dodavatel.objects.get_or_create(
            meno='Global Food Supplies',
            defaults={'email': 'contact@globalfood.com'}
        )

        # 3. Товари
        tovar, _ = Tovar.objects.get_or_create(
            ean_kod='1234567890123',
            defaults={
                'nazov': 'Молоко 1.5%',
                'dodavatel': dodavatel,
                'kriticky_limit': 20
            }
        )

        # 4. Партії (Sarza)
        Sarza.objects.get_or_create(
            id_sarze='BATCH-2026-001',
            tovar=tovar,
            defaults={
                'mnozstvo': 100,
                'datum_exspiracie': datetime.date(2026, 6, 1),
                'aktualna_cena': 35.50
            }
        )

        self.stdout.write(self.style.SUCCESS('База даних успішно заповнена!'))