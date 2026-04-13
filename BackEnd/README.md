# Django Delivery Application Backend

Учебный проект приложения доставки товаров на основе Django и Django REST Framework.

## Стек технологий

- **Django 6.0.4** — веб-фреймворк
- **Django REST Framework 3.17.1** — REST API
- **SQLite** — база данных
- **SessionAuthentication** — авторизация через сессии

## Структура проекта

```
BackEnd/
├── config/                    # Основной конфиг проекта
│   ├── settings.py           # Настройки Django
│   ├── urls.py               # Главные URLs
│   ├── wsgi.py              # WSGI приложение
│   └── asgi.py              # ASGI приложение
├── accounts/                 # Приложение авторизации
│   ├── models.py            # Role, User, Profile
│   ├── views.py             # LoginView, LogoutView
│   ├── urls.py              # URLs для accounts
│   ├── admin.py             # Django Admin
│   └── management/          # Управление данными
│       └── commands/
│           └── initialize_data.py
├── products/                 # Приложение товаров
│   ├── models.py            # Product
│   ├── views.py             # ProductListView, ProductDetailView
│   ├── serializers.py       # ProductSerializer
│   ├── urls.py              # URLs для products
│   └── admin.py             # Django Admin
├── orders/                   # Приложение заказов
│   ├── models.py            # OrderStatus, Order, OrderItem
│   ├── views.py             # OrderListView, OrderCancelView
│   ├── serializers.py       # OrderSerializer, OrderItemSerializer
│   ├── urls.py              # URLs для orders
│   └── admin.py             # Django Admin
├── manage.py                # Django management script
├── db.sqlite3               # База данных SQLite
└── README.md                # Этот файл
```

## Модели данных

### accounts (Аккаунты)

#### Role (Роль)
- `name` — уникальное имя роли (client, courier, support)
- `description` — описание роли

#### User (Пользователь)
- `login` — уникальное имя пользователя
- `password` — хеш пароля
- `role` — ForeignKey на Role

#### Profile (Профиль)
- `user` — OneToOneField на User
- `phone` — телефон (опционально)
- `address` — адрес (опционально)

### products (Товары)

#### Product (Товар)
- `name` — название товара
- `description` — описание
- `price` — цена
- `stock` — количество на складе
- `is_available` — доступен ли товар

### orders (Заказы)

#### OrderStatus (Статус заказа)
- `name` — уникальное имя (new, accepted, in_delivery, delivered, cancelled)

#### Order (Заказ)
- `client` — ForeignKey на User (клиент)
- `courier` — ForeignKey на User (курьер, опционально)
- `status` — ForeignKey на OrderStatus
- `address` — адрес доставки
- `note` — примечание к заказу
- `total_price` — общая стоимость
- `created_at` — время создания
- `updated_at` — время последнего изменения

#### OrderItem (Позиция заказа)
- `order` — ForeignKey на Order
- `product` — ForeignKey на Product
- `quantity` — количество
- `price` — цена товара в момент заказа

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install django djangorestframework
```

### 2. Применение миграций

```bash
python manage.py migrate
```

### 3. Инициализация начальных данных

```bash
python manage.py initialize_data
```

### 4. Создание суперпользователя (для админки)

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится на `http://localhost:8000/`

## API Endpoints

### Авторизация

#### POST `/api/login/`
Вход в систему.

**Request:**
```json
{
    "login": "client_user",
    "password": "password123"
}
```

**Response (200):**
```json
{
    "message": "ok",
    "role": "client"
}
```

#### POST `/api/logout/`
Выход из системы.

**Response (200):**
```json
{
    "message": "Вышли из системы"
}
```

### Товары

#### GET `/api/products/`
Получить список всех доступных товаров.

**Response (200):**
```json
[
    {
        "id": 1,
        "name": "Товар 1",
        "description": "Описание",
        "price": "100.00",
        "stock": 50,
        "is_available": true
    }
]
```

#### GET `/api/products/<id>/`
Получить информацию о конкретном товаре.

### Заказы

#### GET `/api/orders/`
Получить список заказов (фильтруется по роли).

- **client** — видит только свои заказы
- **courier** — видит свободные заказы и заказы, принятые им
- **support** — видит все заказы

**Response (200):**
```json
[
    {
        "id": 1,
        "client": 1,
        "client_login": "client_user",
        "courier": 2,
        "courier_login": "courier_user",
        "status": 1,
        "status_name": "in_delivery",
        "address": "ул. Примерная, 123",
        "note": "Позвонить перед приездом",
        "total_price": "500.00",
        "created_at": "2024-04-12T10:30:00Z",
        "updated_at": "2024-04-12T11:45:00Z",
        "items": [
            {
                "id": 1,
                "product": 1,
                "product_name": "Товар 1",
                "quantity": 2,
                "price": "100.00"
            }
        ]
    }
]
```

#### POST `/api/orders/<id>/cancel/`
Отменить заказ (только для support).

**Response (200):**
```json
{
    "message": "Заказ отменён"
}
```

## Django Admin

Доступ к админ-панели: `http://localhost:8000/admin/`

В админке можно:
- Управлять пользователями и ролями
- Добавлять и редактировать товары
- Просматривать и управлять заказами
- Управлять статусами заказов

## Авторизация

Авторизация осуществляется через **SessionAuthentication**:

1. Пользователь отправляет логин и пароль на `/api/login/`
2. Сервер проверяет пароль и сохраняет `user_id` и `role` в сессии
3. Последующие запросы автоматически включают cookie с ID сессии
4. Для выхода отправляется запрос на `/api/logout/`

## Ролевая модель

- **client** — клиент, может видеть свои заказы
- **courier** — курьер, может видеть свободные и принятые им заказы
- **support** — поддержка, может видеть все заказы и отменять их

## Примеры использования

### Создание пользователя через Django

```python
from accounts.models import User, Role

role = Role.objects.get(name='client')
user = User(login='newuser', role=role)
user.set_password('password123')
user.save()
```

### Создание товара

```python
from products.models import Product

Product.objects.create(
    name='Макароны',
    description='Хорошие макароны',
    price=50.00,
    stock=100
)
```

### Создание заказа

```python
from orders.models import Order, OrderStatus
from accounts.models import User

client = User.objects.get(login='client_user')
status = OrderStatus.objects.get(name='new')
order = Order.objects.create(
    client=client,
    status=status,
    address='ул. Примерная, 123',
    total_price=500.00
)
```

## Возможные расширения

- Добавить создание заказов через API
- Добавить рейтинги и отзывы
- Добавить уведомления
- Добавить отслеживание статуса доставки в реальном времени
- Добавить систему платежей
- Добавить систему промокодов и скидок
