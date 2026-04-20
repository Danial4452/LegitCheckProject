from django.urls import path
from .views import category_list, CategoryDetailView

urlpatterns = [
    path('',      category_list,                name='category-list'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]