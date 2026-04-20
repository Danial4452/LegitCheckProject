from rest_framework import serializers
from .models import Product, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.login', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'text', 'created_at']

class MyCommentSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_serial = serializers.CharField(source='product.serial_number', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'product_name', 'product_serial', 'product_id']

class ProductSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.login', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'is_authentic', 'serial_number', 'manufacture_location', 'history', 'image_url', 'description', 'price', 'stock', 'is_available', 'owner', 'owner_name', 'comments']
        read_only_fields = ['owner']

class ProductLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class ProductPlainSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()

class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
