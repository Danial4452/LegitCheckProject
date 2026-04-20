from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductSearchSerializer

class CheckProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, serial_number):
        try:
            product = Product.objects.get(serial_number=serial_number)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Товар с таким серийным номером не найден.'}, status=status.HTTP_404_NOT_FOUND)

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        from .models import Comment
        comment = Comment.objects.create(product=product, author=request.user, text=text)
        from .serializers import CommentSerializer
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

class MyCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import Comment
        from .serializers import MyCommentSerializer
        comments = Comment.objects.filter(author=request.user)
        return Response(MyCommentSerializer(comments, many=True).data)

class EditCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        from .models import Comment
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
            
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        comment.text = text
        comment.save()
        from .serializers import MyCommentSerializer
        return Response(MyCommentSerializer(comment).data)


class ProductListView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        products = Product.objects.filter(is_available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.owner and product.owner != request.user:
            return Response({'error': 'Вы не можете изменить этот товар'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.owner and product.owner != request.user:
            return Response({'error': 'Вы не можете удалить этот товар'}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# FBV 1: Count products
@api_view(['GET'])
@permission_classes([AllowAny])
def product_count_view(request):
    count = Product.objects.count()
    return Response({"total_products": count})

# FBV 2: Search products
@api_view(['GET'])
@permission_classes([AllowAny])
def product_search_view(request):
    serializer = ProductSearchSerializer(data=request.query_params)
    if serializer.is_valid():
        query = serializer.validated_data['query']
        min_price = serializer.validated_data.get('min_price', 0)
        
        products = Product.objects.filter(name__icontains=query, price__gte=min_price)
        result_serializer = ProductSerializer(products, many=True)
        return Response(result_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

