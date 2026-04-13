# Структура Django проекта — Приложение доставки

## Полное описание файлов и директорий

```
BackEnd/
│
├── config/                              # Основной конфиг проекта
│   ├── __init__.py
│   ├── asgi.py                         # ASGI конфигурация (для async)
│   ├── settings.py                     # Основные настройки Django ⭐
│   ├── urls.py                         # Главные URL routes ⭐
│   └── wsgi.py                         # WSGI конфигурация (для production)
│
├── accounts/                            # Приложение пользователей и авторизации
│   ├── migrations/
│   │   ├── 0001_initial.py             # Первая миграция
│   │   └── __init__.py
│   ├── management/                     # Управление проектом
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   └── initialize_data.py      # Команда инициализации ⭐
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                        # Django Admin конфиг ⭐
│   ├── apps.py
│   ├── models.py                       # Role, User, Profile ⭐
│   ├── tests.py
│   ├── urls.py                         # URLs для accounts ⭐
│   └── views.py                        # LoginView, LogoutView ⭐
│
├── products/                            # Приложение товаров
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                        # Django Admin конфиг ⭐
│   ├── apps.py
│   ├── models.py                       # Product модель ⭐
│   ├── serializers.py                  # Сериализаторы DRF ⭐
│   ├── tests.py
│   ├── urls.py                         # URLs для products ⭐
│   └── views.py                        # ProductListView, ProductDetailView ⭐
│
├── orders/                              # Приложение заказов
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                        # Django Admin конфиг ⭐
│   ├── apps.py
│   ├── models.py                       # Order, OrderItem, OrderStatus ⭐
│   ├── serializers.py                  # Сериализаторы DRF ⭐
│   ├── tests.py
│   ├── urls.py                         # URLs для orders ⭐
│   └── views.py                        # OrderListView, OrderCancelView ⭐
│
├── .gitignore                          # Git ignore файл
├── db.sqlite3                          # SQLite база данных (создается при migrate)
├── manage.py                           # Django management script ⭐
├── requirements.txt                    # Python зависимости ⭐
├── README.md                           # Основное описание проекта ⭐
├── TESTING.md                          # Руководство по тестированию API ⭐
├── PROJECT_STRUCTURE.md                # Этот файл
├── sample_usage.py                     # Пример использования с тестовыми данными ⭐
└── test_api.sh                         # Bash скрипт для тестирования API
```

⭐ = Файлы, которые нужно отредактировать при расширении проекта

## Описание ключевых файлов

### config/settings.py

Основные настройки проекта:

```python
# Приложения
INSTALLED_APPS = [
    'rest_framework',
    'accounts',
    'products',
    'orders',
]

# REST Framework конфигурация
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
```

### config/urls.py

Главные URL routes:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
]
```

### accounts/models.py

Три модели:

```
Role
├── name (CharField, unique)
└── description

User
├── login (CharField, unique)
├── password (CharField)
└── role (ForeignKey → Role)

Profile
├── user (OneToOneField → User)
├── phone
└── address
```

### products/models.py

Одна модель:

```
Product
├── name
├── description
├── price (DecimalField)
├── stock (PositiveIntegerField)
└── is_available (BooleanField)
```

### orders/models.py

Три модели:

```
OrderStatus
└── name (CharField, unique)
    ├── 'new'
    ├── 'accepted'
    ├── 'in_delivery'
    ├── 'delivered'
    └── 'cancelled'

Order
├── client (ForeignKey → User)
├── courier (ForeignKey → User, nullable)
├── status (ForeignKey → OrderStatus)
├── address
├── note
├── total_price
├── created_at
└── updated_at

OrderItem
├── order (ForeignKey → Order)
├── product (ForeignKey → Product)
├── quantity
└── price
```

### accounts/views.py

Два API view:

```
LoginView (APIView)
└── POST /api/login/
    ├── Input: {login, password}
    └── Output: {message, role}

LogoutView (APIView)
└── POST /api/logout/
    └── Output: {message}
```

### products/views.py

Два API view:

```
ProductListView (APIView)
└── GET /api/products/
    └── Output: [Product, ...]

ProductDetailView (APIView)
└── GET /api/products/<id>/
    └── Output: Product
```

### orders/views.py

Два API view:

```
OrderListView (APIView)
└── GET /api/orders/
    ├── role=client    → orders where client_id=user_id
    ├── role=courier   → orders where courier_id=user_id or courier_id is null
    └── role=support   → all orders

OrderCancelView (APIView)
└── POST /api/orders/<id>/cancel/
    ├── Only for role='support'
    └── Output: {message}
```

## Поток данных API

### Вход в систему

```
Client
  │
  ├─→ POST /api/login/
  │   {login: "ivan", password: "password123"}
  │
Server
  ├─→ Hash пароль с помощью check_password()
  ├─→ Проверить совпадение
  ├─→ Сохранить user_id и role в session
  │
Client ←─ {message: "ok", role: "client"}
  │
  └─→ Куки sessionid сохраняются браузером
```

### Получение заказов

```
Client (авторизован)
  │
  ├─→ GET /api/orders/
  │   (header: Cookie: sessionid=xxx)
  │
Server
  ├─→ Прочитать user_id и role из session
  ├─→ Отфильтровать заказы по роли
  ├─→ Сериализовать данные
  │
Client ←─ [Order, ...]
```

## Команды для разработки

### Начальная установка

```bash
# 1. Установить зависимости
pip install django djangorestframework

# 2. Создать миграции
python manage.py makemigrations

# 3. Применить миграции
python manage.py migrate

# 4. Инициализировать начальные данные
python manage.py initialize_data

# 5. Создать суперпользователя для админки
python manage.py createsuperuser

# 6. Создать тестовые данные
python sample_usage.py

# 7. Запустить сервер
python manage.py runserver
```

### Разработка

```bash
# Создать новую миграцию после изменения models.py
python manage.py makemigrations app_name

# Применить миграции
python manage.py migrate

# Запустить Django shell (интерактивное окружение)
python manage.py shell

# Запустить тесты (если есть)
python manage.py test

# Собрать статические файлы (для production)
python manage.py collectstatic

# Создать резервную копию базы
python manage.py dumpdata > backup.json

# Восстановить базу из резервной копии
python manage.py loaddata backup.json
```

## Расширение проекта

### Добавить новый API endpoint

1. **Создать view в `app/views.py`:**
   ```python
   from rest_framework.views import APIView
   from rest_framework.response import Response

   class MyView(APIView):
       def get(self, request):
           return Response({'message': 'hello'})
   ```

2. **Добавить URL в `app/urls.py`:**
   ```python
   path('myendpoint/', MyView.as_view())
   ```

3. **Добавить в `config/urls.py`:**
   ```python
   path('api/', include('app.urls'))
   ```

4. **Запустить сервер:**
   ```bash
   python manage.py runserver
   ```

### Добавить новую модель

1. **Создать в `app/models.py`**
2. **Запустить миграцию:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Создать сериализатор в `app/serializers.py`**
4. **Создать view в `app/views.py`**
5. **Добавить URL в `app/urls.py`**

### Добавить авторизацию JWT (опционально)

1. Установить: `pip install djangorestframework-simplejwt`
2. Изменить в `settings.py`:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
   }
   ```
3. Добавить URLs для токен-эндпоинтов

## Тестирование

### Используя curl

```bash
# Получить товары
curl http://localhost:8000/api/products/

# Вход
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"login":"ivan","password":"password123"}' \
  -c cookies.txt

# Заказы (с сохраненными куками)
curl http://localhost:8000/api/orders/ -b cookies.txt
```

### Используя Python

```python
import requests

session = requests.Session()

# Вход
response = session.post('http://localhost:8000/api/login/', json={
    'login': 'ivan',
    'password': 'password123'
})

# Заказы
response = session.get('http://localhost:8000/api/orders/')
print(response.json())
```

### Используя Django shell

```python
python manage.py shell

# Создать пользователя
from accounts.models import User, Role
role = Role.objects.get(name='client')
user = User(login='test', role=role)
user.set_password('password123')
user.save()

# Проверить пароль
from django.contrib.auth.hashers import check_password
user = User.objects.get(login='test')
check_password('password123', user.password)  # True
```

## Ограничения текущей реализации

1. **Нет механизма создания заказов через API** — только просмотр
2. **Нет изменения статуса заказа курьером** — только support может отменять
3. **Нет системы платежей** — заказы создаются с заранее известной ценой
4. **Нет уведомлений** — нет отправки email или SMS
5. **Нет истории изменений** — не отслеживаются изменения заказов
6. **Нет файловых загрузок** — нет возможности загружать фотографии товаров
7. **Нет таблицы логирования** — действия пользователей не логируются

## Возможные улучшения

1. Добавить создание и редактирование заказов через API
2. Добавить система рейтингования товаров
3. Добавить фильтрацию и поиск товаров
4. Добавить расчет доставки на основе расстояния
5. Добавить систему скидок и промокодов
6. Добавить интеграцию с системой платежей (Stripe, Yandex.Kassa)
7. Добавить WebSocket для отслеживания заказов в реальном времени
8. Добавить систему уведомлений (email, SMS, push)
9. Добавить документирование API с помощью Swagger/OpenAPI
10. Добавить систему логирования действий пользователей
