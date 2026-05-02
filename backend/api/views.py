from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import StockService, OrderService, ExpirationService
from .serializers import SarzaSerializer, OrderSerializer

# UC01: Прийом нової партії
class ReceiveBatchView(APIView):
    def post(self, request):
        try:
            # Викликаємо сервіс, який ми написали раніше
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

# UC02: Запуск Smart-Reorder
class SmartReorderView(APIView):
    def post(self, request):
        orders = OrderService.generate_smart_reorder()
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "message": f"Vytvorených {len(orders)} návrhov objednávok",
            "orders": serializer.data
        }, status=status.HTTP_201_CREATED)

# UC03: Список товарів, що скоро прострочаться
class ExpiringSoonView(APIView):
    def get(self, request):
        days = int(request.query_params.get('days', 2))
        items = ExpirationService.get_expiring_soon(days=days)
        serializer = SarzaSerializer(items, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        # Знижка для конкретної партії
        discount = request.data.get('discount', 50)
        updated_sarza = ExpirationService.apply_batch_discount(pk, discount)
        return Response({"message": "Cena aktualizovaná", "new_price": updated_sarza.aktualna_cena})




# UC04: Інвентурні гремліни вперед
class InventoryCheckView(APIView):
    # Почати нову інвентаризацію
    def post(self, request):
        kategoria = request.data.get('kategoria', 'Všetko')
        inventura = InventoryService.start_inventory(request.user, kategoria)
        serializer = InventuraSerializer(inventura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Просканувати товар у межах інвентаризації
    def patch(self, request, pk):
        # pk тут - це ID інвентаризації
        tovar_id = request.data.get('tovar_id')
        real_qty = int(request.data.get('real_qty', 0))

        try:
            result = InventoryService.record_item_check(pk, tovar_id, real_qty)
            return Response(result, status=status.HTTP_200_OK)
        except Tovar.DoesNotExist:
            return Response({"error": "Tovar nenájdený (Výnimka 1)"}, status=status.HTTP_404_NOT_FOUND)