from rest_framework import serializers
from .models import Product

from Comment.models import Comment

# ModelSerializer
class ProductSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_comments(self, obj):
        comments = Comment.objects.filter(product=obj).select_related('author').order_by('-created_at')
        return [
            {
                'id': c.id,
                'text': c.text,
                'author_name': c.author.username,
                'created_at': c.created_at
            } for c in comments
        ]


# Serializer — для поиска/фильтрации (не ModelSerializer)
class ProductFilterSerializer(serializers.Serializer):
    category = serializers.IntegerField(required=False)
    is_authentic = serializers.BooleanField(required=False)