from django.urls import path
from .views import comment_list, CommentDetailView

urlpatterns = [
    path('product/<int:product_id>/', comment_list,               name='comment-list'),
    path('<int:pk>/',                 CommentDetailView.as_view(), name='comment-detail'),
]