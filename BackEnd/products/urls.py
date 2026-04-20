from django.urls import path
from .views import ProductListView, ProductDetailView, product_count_view, product_search_view, CheckProductView, AddCommentView, MyCommentsView, EditCommentView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/count/', product_count_view, name='product-count'),
    path('products/search/', product_search_view, name='product-search'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/comments/', AddCommentView.as_view(), name='product-add-comment'),
    path('check/<str:serial_number>/', CheckProductView.as_view(), name='product-check'),
    path('my-comments/', MyCommentsView.as_view(), name='my-comments'),
    path('comments/<int:comment_id>/', EditCommentView.as_view(), name='edit-comment'),
]
