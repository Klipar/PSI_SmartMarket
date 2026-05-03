from rest_framework import serializers
# Додаємо Inventura та ProtokolInventury в список імпортів нижче:
from .models import Tovar, Sarza, NavrhObjednavky, User, Inventura, ProtokolInventury

class TovarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tovar
        fields = '__all__'

class SarzaSerializer(serializers.ModelSerializer):
    tovar_nazov = serializers.ReadOnlyField(source='tovar.nazov')

    class Meta:
        model = Sarza
        fields = ['id', 'tovar', 'tovar_nazov', 'id_sarze', 'mnozstvo', 'datum_exspiracie', 'aktualna_cena']

class OrderSerializer(serializers.ModelSerializer):
    # Отримуємо ім'я постачальника з пов'язаної моделі Dodavatel
    dodavatel_meno = serializers.ReadOnlyField(source='dodavatel.meno')
    # Рахуємо кількість позицій у замовленні
    items_count = serializers.SerializerMethodField()
    # Рахуємо загальну суму замовлення
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = NavrhObjednavky
        fields = ['id', 'stav', 'datum_vytvorenia', 'dodavatel', 'dodavatel_meno', 'items_count', 'total_price']

    def get_items_count(self, obj):
        # Рахуємо кількість PolozkaNavrhu для цього замовлення
        return obj.polozky.count()

    def get_total_price(self, obj):
        # Сумуємо (ціна * кількість) для всіх позицій
        from django.db.models import F, Sum
        total = obj.polozky.aggregate(
            total=Sum(F('mnozstvo') * F('cena_pri_objednavke'))
        )['total']
        return float(total) if total else 0.0

class InventuraSerializer(serializers.ModelSerializer):
    vykonal_meno = serializers.ReadOnlyField(source='vykonal.username')

    class Meta:
        model = Inventura
        fields = ['id', 'datum_zahajenia', 'kategoria', 'vykonal', 'vykonal_meno']

class ProtokolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtokolInventury
        fields = '__all__'