from django.db import models
from LegitCheckProject.BackEnd.accounts.models import User
from LegitCheckProject.BackEnd.products.models import Product


class OrderStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_as_client'
    )
    courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders_as_courier'
    )
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    address = models.TextField()
    note = models.TextField(blank=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} — {self.client.login}'

    def cancel(self):
        cancelled = OrderStatus.objects.get(name='cancelled')
        self.status = cancelled
        self.courier = None
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

