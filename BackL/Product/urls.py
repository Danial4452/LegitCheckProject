from django.urls import path
from .views import product_list, product_filter, ProductDetailView

urlpatterns = [
    path('',           product_list,              name='product-list'),
    path('filter/',    product_filter,             name='product-filter'),
    path('<int:pk>/',  ProductDetailView.as_view(), name='product-detail'),
]