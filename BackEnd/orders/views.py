from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Order
from .serializers import OrderSerializer


class OrderListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        role = request.data.get('role')
        user_id = request.data.get('user_id')

        if not role or not user_id:
            return Response(
                {'error': 'Укажите user_id и role'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if role == 'client':
            orders = Order.objects.filter(client_id=user_id)
        elif role == 'courier':
            orders = Order.objects.filter(
                Q(courier__isnull=True) | Q(courier_id=user_id)
            )
        elif role == 'support':
            orders = Order.objects.all()
        else:
            return Response(
                {'error': 'Неизвестная роль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderCancelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, order_id):
        user_id = request.data.get('user_id')
        role = request.data.get('role')

        if not user_id or not role:
            return Response(
                {'error': 'Укажите user_id и role'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if role != 'support':
            return Response(
                {'error': 'Только support может отменять заказы'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        order.cancel()

        return Response({'message': 'Заказ отменён'})

