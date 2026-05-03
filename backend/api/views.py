from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .services import StockService, OrderService, ExpirationService, InventoryService
from .serializers import SarzaSerializer, NavrhObjednavkySerializer, InventuraSerializer
from .models import NavrhObjednavky, Tovar

# --- UC01: ПРИЙОМ ТОВАРУ ---
class ReceiveBatchView(APIView):
    @extend_schema(
        summary="Прийом нової партії (UC01)",
        request=inline_serializer(
            name='ReceiveBatchRequest',
            fields={
                'ean': serializers.CharField(),
                'batch_id': serializers.CharField(),
                'quantity': serializers.IntegerField(),
                'expiration_date': serializers.DateField(),
                'price': serializers.DecimalField(max_digits=10, decimal_places=2)
            }
        ),
        responses={201: SarzaSerializer}
    )
    def post(self, request):
        try:
            new_sarza = StockService.receive_new_batch(
                ean_code=request.data.get('ean'),
                batch_id=request.data.get('batch_id'),
                quantity=request.data.get('quantity'),
                expiration_date=request.data.get('expiration_date'),
                price=request.data.get('price')
            )
            serializer = SarzaSerializer(new_sarza)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- UC02: SMART REORDER ---
class SmartReorderView(APIView):
    @extend_schema(
        summary="Авто-створення замовлень (UC02)",
        responses={201: NavrhObjednavkySerializer(many=True)}
    )
    def post(self, request):
        orders = OrderService.generate_smart_reorder()
        serializer = NavrhObjednavkySerializer(orders, many=True)
        return Response({
            "message": f"Vytvorených {len(orders)} návrhov objednávok",
            "orders": serializer.data
        }, status=status.HTTP_201_CREATED)


# --- UC03: ЕКСПІРАЦІЯ ТА ЗНИЖКИ ---
class ExpiringSoonView(APIView):
    @extend_schema(summary="Список товарів, що прострочуються (UC03)")
    def get(self, request):
        days = int(request.query_params.get('days', 2))
        items = ExpirationService.get_expiring_soon(days=days)
        serializer = SarzaSerializer(items, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Застосувати знижку до партії (UC03)",
        request=inline_serializer(
            name='DiscountRequest',
            fields={'discount': serializers.IntegerField(default=50)}
        )
    )
    def patch(self, request, pk):
        # Переконайтеся, що в urls.py цей маршрут має <int:pk>
        discount = request.data.get('discount', 50)
        updated_sarza = ExpirationService.apply_batch_discount(pk, discount)
        return Response({
            "message": "Cena aktualizovaná",
            "new_price": str(updated_sarza.aktualna_cena)
        })


# --- UC04: ІНВЕНТАРИЗАЦІЯ ---
class InventoryStartView(APIView):
    @extend_schema(
        summary="Почати інвентаризацію (UC04 Крок 1)",
        request=inline_serializer(
            name='StartInventoryRequest',
            fields={'kategoria': serializers.CharField(default='Všetko')}
        ),
        responses={201: InventuraSerializer}
    )
    def post(self, request):
        kategoria = request.data.get('kategoria', 'Všetko')
        # Для тестів, якщо немає авторизації, можна передати None або системного юзера
        user = request.user if request.user.is_authenticated else None
        inventura = InventoryService.start_inventory(user, kategoria)
        serializer = InventuraSerializer(inventura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryRecordView(APIView):
    @extend_schema(
        summary="Записати перевірку товару (UC04 Крок 3)",
        request=inline_serializer(
            name='RecordCheckRequest',
            fields={
                'tovar_id': serializers.IntegerField(),
                'real_qty': serializers.IntegerField()
            }
        )
    )
    def patch(self, request, pk):
        """pk — це ID поточної інвентаризації"""
        tovar_id = request.data.get('tovar_id')
        real_qty = int(request.data.get('real_qty', 0))

        try:
            result = InventoryService.record_item_check(pk, tovar_id, real_qty)
            return Response(result, status=status.HTTP_200_OK)
        except Tovar.DoesNotExist:
            return Response({"error": "Tovar nenájdený"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from .serializers import NavrhObjednavkySerializer # Переконайся, що імпортував оновлений серіалізатор
from .models import NavrhObjednavky

# Додаємо цей клас
class OrderListView(APIView):
    @extend_schema(
        summary="Отримати список усіх замовлень",
        responses={200: NavrhObjednavkySerializer(many=True)}
    )
    def get(self, request):
        orders = NavrhObjednavky.objects.all().order_by('-datum_vytvorenia')
        serializer = NavrhObjednavkySerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    def patch(self, request, pk):
        # 5.1 Úprava množstva або Зміна статусу
        try:
            order = NavrhObjednavky.objects.get(pk=pk)
            action = request.data.get('action')

            if action == 'confirm':
                # Головний сценарій крок 6-7: Potvrdiť a odoslať
                order.stav = 'Odoslané'
                order.save()
                return Response({"message": "Objednávka odoslaná"})

            elif action == 'update_item':
                # 5.1 Úprava množstva
                item_id = request.data.get('item_id')
                new_qty = request.data.get('quantity')
                polozka = PolozkaObjednavky.objects.get(id=item_id, objednavka=order)
                polozka.navrhovane_mnozstvo = new_qty
                polozka.save()
                return Response({"message": "Množstvo upravené"})

        except NavrhObjednavky.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk):
        # 6.1 Zamietnutie návrhu
        NavrhObjednavky.objects.filter(pk=pk).delete()
        return Response({"message": "Návrh vymazaný"})


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NavrhObjednavky, PolozkaObjednavky
from .serializers import NavrhObjednavkySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = NavrhObjednavky.objects.all().order_by('-datum_vytvorenia')
    serializer_name = NavrhObjednavkySerializer

    # UC02: Крок 6-7 (Підтвердження)
    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        order.stav = 'OD' # Odoslané
        order.save()
        return Response({'status': 'order confirmed'})

    # UC02: Сценарій 5.1 (Оновлення кількості в позиції)
    @action(detail=True, methods=['patch'])
    def update_item_quantity(self, request, pk=None):
        item_id = request.data.get('item_id')
        new_qty = request.data.get('quantity')
        try:
            item = PolozkaObjednavky.objects.get(id=item_id, objednavka_id=pk)
            item.navrhovane_mnozstvo = new_qty
            item.save()
            return Response({'status': 'quantity updated'})
        except PolozkaObjednavky.DoesNotExist:
            return Response(status=404)