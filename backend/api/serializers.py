from rest_framework import serializers
from .models import Tovar, Sarza, NavrhObjednavky, PolozkaObjednavky, Inventura, ProtokolInventury
from rest_framework import serializers
from django.db.models import Sum, F
class TovarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tovar
        fields = '__all__'

class SarzaSerializer(serializers.ModelSerializer):
    tovar_nazov = serializers.ReadOnlyField(source='tovar.nazov')

    class Meta:
        model = Sarza
        fields = ['id', 'tovar', 'tovar_nazov', 'id_sarze', 'mnozstvo', 'datum_exspiracie', 'aktualna_cena']


class InventuraSerializer(serializers.ModelSerializer):
    vykonal_meno = serializers.ReadOnlyField(source='vykonal.username')

    class Meta:
        model = Inventura
        fields = ['id', 'datum_zahajenia', 'kategoria', 'vykonal', 'vykonal_meno']

class ProtokolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtokolInventury
        fields = '__all__'

class PolozkaObjednavkySerializer(serializers.ModelSerializer):
    tovar_name = serializers.ReadOnlyField(source='tovar.nazov')

    class Meta:
        model = PolozkaObjednavky
        # Використовуємо реальні назви полів з моделі
        fields = ['id', 'tovar', 'tovar_name', 'navrhovane_mnozstvo', 'cena_za_kus']

class NavrhObjednavkySerializer(serializers.ModelSerializer):
    polozky = PolozkaObjednavkySerializer(many=True, read_only=True)
    supplier_name = serializers.ReadOnlyField(source='dodavatel.meno')
    items_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = NavrhObjednavky
        fields = ['id', 'stav', 'supplier_name', 'datum_vytvorenia', 'polozky', 'items_count', 'total_price']

    def get_items_count(self, obj):
        return obj.polozky.count()

    def get_total_price(self, obj):
        # ВИПРАВЛЕНО: використовуємо 'navrhovane_mnozstvo' та 'cena_za_kus'
        result = obj.polozky.aggregate(
            total=Sum(F('navrhovane_mnozstvo') * F('cena_za_kus'))
        )['total']
        return result or 0