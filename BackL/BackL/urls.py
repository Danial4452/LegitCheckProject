from django.contrib import admin
from django.urls import path, include
from Product.views import check_product
from Comment.views import my_comments, all_comments

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('api/auth/',     include('accounts.urls')),
    path('api/categories/', include('Category.urls')),
    path('api/products/',   include('Product.urls')),
    path('api/comments/',   include('Comment.urls')),
    path('api/my-comments/', my_comments, name='my-comments'),
    path('api/all-comments/', all_comments, name='all-comments'),
    path('api/check/<str:serial_number>/', check_product, name='check-product'),
]