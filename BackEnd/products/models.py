from django.db import models


from accounts.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, default="Unknown")
    is_authentic = models.BooleanField(default=True)
    serial_number = models.CharField(max_length=100, unique=True, default="000000")
    manufacture_location = models.CharField(max_length=255, blank=True)
    history = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    
    # Old fields we might still need or can keep optional
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.login} on {self.product.name}"

