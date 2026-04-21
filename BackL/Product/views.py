from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer, ProductFilterSerializer
from permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def check_product(request, serial_number):
    try:
        product = Product.objects.get(serial_number=serial_number)
        return Response(ProductSerializer(product).data)
    except Product.DoesNotExist:
        return Response({'error': 'Товар с таким кодом не найден в базе данных.'}, status=status.HTTP_404_NOT_FOUND)

# Product/views.py

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    if request.method == 'GET':
        if request.user.is_staff:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(owner=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_staff:
            return Response(
            {'error': 'Только админ может добавлять продукты'},
            status=status.HTTP_403_FORBIDDEN
        )
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FBV — фильтрация продуктов
@api_view(['GET'])
def product_filter(request):
    serializer = ProductFilterSerializer(data=request.query_params)
    if serializer.is_valid():
        queryset = Product.objects.all()
        if serializer.validated_data.get('brand'):
            queryset = queryset.filter(brand=serializer.validated_data['brand'])
        if serializer.validated_data.get('category'):
            queryset = queryset.filter(category=serializer.validated_data['category'])
        if 'is_authentic' in serializer.validated_data:
            queryset = queryset.filter(is_authentic=serializer.validated_data['is_authentic'])
        return Response(ProductSerializer(queryset, many=True).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, product) 
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, product) 
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, product)  
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
