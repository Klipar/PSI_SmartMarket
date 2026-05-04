from rest_framework import serializers
from .models import Tovar, Sarza, NavrhObjednavky, PolozkaObjednavky, Inventura, ProtokolInventury

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
    tovar_name = serializers.CharField(source='tovar.nazov', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = PolozkaObjednavky
        fields = ['id', 'tovar', 'tovar_name', 'navrhovane_mnozstvo', 'cena_za_kus', 'subtotal']

    def get_subtotal(self, obj):
        if obj.cena_za_kus is None or obj.navrhovane_mnozstvo is None:
            return 0.0
        return float(obj.cena_za_kus) * obj.navrhovane_mnozstvo

class NavrhObjednavkySerializer(serializers.ModelSerializer):
    polozky = PolozkaObjednavkySerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = NavrhObjednavky
        fields = [
            'id', 'stav', 'supplier_name', 'items_count',
            'total_price', 'polozky', 'datum_vytvorenia'
        ]