from django.contrib import admin
from .models import OrderStatus, Order, OrderItem


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'courier', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__login', 'courier__login']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']

