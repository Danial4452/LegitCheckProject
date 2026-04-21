from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from permissions import IsOwnerOrAdmin

# FBV — список комментариев к продукту
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, product_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(product_id=product_id)
        return Response(CommentSerializer(comments, many=True).data)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, comment)  
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_comments(request):
    comments = Comment.objects.filter(author=request.user)
    data = []
    for c in comments:
        data.append({
            'id': c.id,
            'text': c.text,
            'product_name': c.product.name,
            'product_serial': c.product.serial_number,
            'created_at': c.created_at
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_comments(request):
    if not request.user.is_staff:
        return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)
    comments = Comment.objects.all()
    data = []
    for c in comments:
        data.append({
            'id': c.id,
            'text': c.text,
            'product_name': c.product.name,
            'product_serial': c.product.serial_number,
            'created_at': c.created_at,
            'author_name': c.author.username
        })
    return Response(data)

