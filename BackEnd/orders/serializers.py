from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client_login = serializers.CharField(source='client.login', read_only=True)
    courier_login = serializers.CharField(source='courier.login', read_only=True, allow_null=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'client_login',
            'courier',
            'courier_login',
            'status',
            'status_name',
            'address',
            'note',
            'total_price',
            'created_at',
            'updated_at',
            'items'
        ]
