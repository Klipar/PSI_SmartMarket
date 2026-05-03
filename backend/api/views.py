from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .services import StockService, OrderService, ExpirationService, InventoryService
from .serializers import SarzaSerializer, OrderSerializer, InventuraSerializer
from .models import Tovar

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
        responses={201: OrderSerializer(many=True)}
    )
    def post(self, request):
        orders = OrderService.generate_smart_reorder()
        serializer = OrderSerializer(orders, many=True)
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