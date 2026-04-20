from django.db import models
from django.contrib.auth.models import User
from Category.models import Category


class Product(models.Model):
    # Связи
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    # Поля из твоего интерфейса
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    is_authentic = models.BooleanField(default=False)
    serial_number = models.CharField(max_length=100, unique=True)
    manufacture_location = models.CharField(max_length=255)
    history = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # optional (?)

    # Служебные поля
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"

    class Meta:
        ordering = ['-created_at']

