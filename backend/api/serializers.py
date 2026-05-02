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
    class Meta:
        model = NavrhObjednavky
        fields = '__all__'

class InventuraSerializer(serializers.ModelSerializer):
    vykonal_meno = serializers.ReadOnlyField(source='vykonal.username')

    class Meta:
        model = Inventura
        fields = ['id', 'datum_zahajenia', 'kategoria', 'vykonal', 'vykonal_meno']

class ProtokolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtokolInventury
        fields = '__all__'