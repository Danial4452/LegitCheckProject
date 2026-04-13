"""
Пример использования Django API через Python.

Запустите сервер перед запуском этого скрипта:
    python manage.py runserver
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from LegitCheckProject.BackEnd.accounts.models import User, Role, Profile
from LegitCheckProject.BackEnd.products.models import Product
from LegitCheckProject.BackEnd.orders.models import Order, OrderStatus, OrderItem


def create_test_users():
    """Создать тестовых пользователей"""
    print("\n=== Создание тестовых пользователей ===")
    
    client_role = Role.objects.get(name='client')
    courier_role = Role.objects.get(name='courier')
    
    # Client user
    client = User(login='ivan', role=client_role)
    client.set_password('password123')
    client.save()
    
    profile = Profile.objects.create(
        user=client,
        phone='+79991234567',
        address='Москва, ул. Примерная, 123'
    )
    
    print(f"✓ Создан клиент: {client.login}")
    
    # Courier user
    courier = User(login='vova', role=courier_role)
    courier.set_password('password123')
    courier.save()
    
    profile = Profile.objects.create(
        user=courier,
        phone='+79997654321',
        address='Москва, ул. Доставки, 456'
    )
    
    print(f"✓ Создан курьер: {courier.login}")


def create_test_products():
    """Создать тестовые товары"""
    print("\n=== Создание тестовых товаров ===")
    
    products_data = [
        ('Молоко', 'Свежее коровье молоко 1л', Decimal('80.00'), 50),
        ('Хлеб', 'Белый хлеб', Decimal('30.00'), 100),
        ('Яблоки', 'Краснобочка, кг', Decimal('120.00'), 30),
        ('Сыр', 'Плавленый сыр', Decimal('150.00'), 20),
        ('Кефир', 'Кефир 1л', Decimal('70.00'), 40),
    ]
    
    for name, description, price, stock in products_data:
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        print(f"✓ Товар: {product.name} ({product.price}₽)")


def create_test_orders():
    """Создать тестовый заказ"""
    print("\n=== Создание тестовых заказов ===")
    
    client = User.objects.get(login='ivan')
    new_status = OrderStatus.objects.get(name='new')
    courier = User.objects.get(login='vova')
    in_delivery = OrderStatus.objects.get(name='in_delivery')
    
    # Заказ 1: новый (без курьера)
    order1 = Order.objects.create(
        client=client,
        status=new_status,
        address='Москва, ул. Примерная, 123',
        note='Позвонить перед приездом',
        total_price=Decimal('230.00')
    )
    
    # Добавляем товары
    product1 = Product.objects.get(name='Молоко')
    product2 = Product.objects.get(name='Хлеб')
    
    OrderItem.objects.create(
        order=order1,
        product=product1,
        quantity=2,
        price=product1.price
    )
    
    OrderItem.objects.create(
        order=order1,
        product=product2,
        quantity=1,
        price=product2.price
    )
    
    print(f"✓ Заказ #{order1.id}: новый")
    
    # Заказ 2: в доставке (с курьером)
    order2 = Order.objects.create(
        client=client,
        courier=courier,
        status=in_delivery,
        address='Москва, ул. Примерная, 123',
        total_price=Decimal('120.00')
    )
    
    product3 = Product.objects.get(name='Яблоки')
    OrderItem.objects.create(
        order=order2,
        product=product3,
        quantity=1,
        price=product3.price
    )
    
    print(f"✓ Заказ #{order2.id}: в доставке")


def print_database_stats():
    """Вывести статистику базы данных"""
    print("\n=== Статистика базы данных ===")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Товаров: {Product.objects.count()}")
    print(f"Заказов: {Order.objects.count()}")
    print(f"Позиций в заказах: {OrderItem.objects.count()}")


if __name__ == '__main__':
    try:
        # Очистить старые данные (опционально)
        # User.objects.filter(login__in=['ivan', 'vova']).delete()
        # Product.objects.all().delete()
        
        # Создать тестовые данные
        create_test_users()
        create_test_products()
        create_test_orders()
        print_database_stats()
        
        print("\n✓ Тестовые данные созданы!")
        print("\nСейчас вы можете тестировать API:")
        print("  python manage.py runserver")
        print("\nЭндпоинты:")
        print("  POST /api/login/ - вход в систему")
        print("  POST /api/logout/ - выход из системы")
        print("  GET /api/products/ - список товаров")
        print("  GET /api/orders/ - список заказов")
        print("  POST /api/orders/<id>/cancel/ - отменить заказ")
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
