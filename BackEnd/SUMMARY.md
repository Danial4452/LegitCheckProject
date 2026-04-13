# Резюме проекта — Django Delivery App

## 🎯 Задача

Создать учебный Django REST API проект приложения доставки товаров с авторизацией через сессии.

## ✅ Что было реализовано

### Основная структура

- **Django проект** с правильной структурой
- **3 приложения Django**: accounts, products, orders
- **SQLite база данных** с 6 моделями
- **REST API** с 6 эндпоинтами
- **SessionAuthentication** для авторизации (без JWT)

### Приложение accounts

**Модели:**
- `Role` — справочник ролей (client, courier, support)
- `User` — пользователи с хешированными паролями
- `Profile` — расширенная информация пользователя

**Views:**
- `LoginView (POST /api/login/)` — вход с логином и паролем
- `LogoutView (POST /api/logout/)` — выход с очисткой сессии

### Приложение products

**Модели:**
- `Product` — товары с ценой, количеством, доступностью

**Views:**
- `ProductListView (GET /api/products/)` — список доступных товаров
- `ProductDetailView (GET /api/products/<id>/)` — информация о товаре

**Сериализаторы:**
- `ProductSerializer` — преобразование моделей в JSON

### Приложение orders

**Модели:**
- `OrderStatus` — справочник статусов заказов
- `Order` — заказы с клиентом, курьером, статусом, адресом
- `OrderItem` — позиции заказа с товарами и количеством

**Views:**
- `OrderListView (GET /api/orders/)` — список заказов с фильтрацией по ролям
- `OrderCancelView (POST /api/orders/<id>/cancel/)` — отмена заказа (только support)

**Сериализаторы:**
- `OrderSerializer` — сериализация заказов
- `OrderItemSerializer` — сериализация позиций заказа

### Конфигурация

**config/settings.py:**
```python
INSTALLED_APPS = [
    'rest_framework',
    'accounts',
    'products',
    'orders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
```

**config/urls.py:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
]
```

## 📁 Структура файлов

```
BackEnd/
├── README.md ........................ Основная документация проекта
├── QUICKSTART.md ................... Быстрый старт
├── TESTING.md ....................... Руководство по тестированию
├── PROJECT_STRUCTURE.md ............ Детальная структура проекта
├── SUMMARY.md (этот файл)
├── requirements.txt ................ Зависимости (Django, DRF)
├── sample_usage.py ................. Создание тестовых данных
├── test_api.sh ..................... Bash скрипт для тестирования
├── db.sqlite3 ...................... База данных (создается при migrate)
├── manage.py ....................... Django management script
│
├── config/
│   ├── __init__.py
│   ├── settings.py ................ Основные настройки Django
│   ├── urls.py .................... Главные URL-маршруты
│   ├── wsgi.py .................... WSGI конфигурация
│   └── asgi.py .................... ASGI конфигурация
│
├── accounts/
│   ├── __init__.py
│   ├── models.py .................. Role, User, Profile
│   ├── views.py ................... LoginView, LogoutView
│   ├── urls.py .................... URL-маршруты для accounts
│   ├── admin.py ................... Django Admin конфигурация
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── initialize_data.py .. Инициализация ролей и статусов
│
├── products/
│   ├── __init__.py
│   ├── models.py .................. Product
│   ├── views.py ................... ProductListView, ProductDetailView
│   ├── serializers.py ............ ProductSerializer
│   ├── urls.py .................... URL-маршруты для products
│   ├── admin.py ................... Django Admin конфигурация
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│       ├── 0001_initial.py
│       └── __init__.py
│
└── orders/
    ├── __init__.py
    ├── models.py .................. OrderStatus, Order, OrderItem
    ├── views.py ................... OrderListView, OrderCancelView
    ├── serializers.py ............ OrderSerializer, OrderItemSerializer
    ├── urls.py .................... URL-маршруты для orders
    ├── admin.py ................... Django Admin конфигурация
    ├── apps.py
    ├── tests.py
    └── migrations/
        ├── 0001_initial.py
        └── __init__.py
```

## 🔗 API Endpoints

| Метод | Endpoint | Описание | Auth | Роли |
|-------|----------|---------|------|------|
| POST | `/api/login/` | Вход в систему | ✗ | - |
| POST | `/api/logout/` | Выход из системы | ✗ | - |
| GET | `/api/products/` | Список товаров | ✗ | - |
| GET | `/api/products/<id>/` | Информация о товаре | ✗ | - |
| GET | `/api/orders/` | Список заказов | ✓ | client, courier, support |
| POST | `/api/orders/<id>/cancel/` | Отменить заказ | ✓ | support |

## 👥 Ролевая модель

- **client** — может видеть только свои заказы
- **courier** — видит свободные заказы и заказы, принятые им
- **support** — видит все заказы и может их отменять

## 🗄️ Структура базы данных

### Таблица Role
```sql
id | name    | description
1  | client  | Клиент
2  | courier | Курьер
3  | support | Поддержка
```

### Таблица User
```sql
id | login | password | role_id
1  | ivan  | hashed   | 1
2  | vova  | hashed   | 2
```

### Таблица Profile
```sql
id | user_id | phone        | address
1  | 1       | +7999... | Москва, ул. Примерная, 123
2  | 2       | +7999... | Москва, ул. Доставки, 456
```

### Таблица Product
```sql
id | name  | price  | stock | is_available
1  | Молоко| 80.00  | 50    | true
2  | Хлеб  | 30.00  | 100   | true
```

### Таблица OrderStatus
```sql
id | name
1  | new
2  | accepted
3  | in_delivery
4  | delivered
5  | cancelled
```

### Таблица Order
```sql
id | client_id | courier_id | status_id | address | total_price
1  | 1         | NULL       | 1         | Адрес   | 230.00
2  | 1         | 2          | 3         | Адрес   | 120.00
```

### Таблица OrderItem
```sql
id | order_id | product_id | quantity | price
1  | 1        | 1          | 2        | 80.00
2  | 1        | 2          | 1        | 30.00
3  | 2        | 3          | 1        | 120.00
```

## 🧪 Тестовые данные

При запуске `python sample_usage.py` создаются:

**Пользователи:**
- `ivan:password123` (роль: client)
- `vova:password123` (роль: courier)

**Товары:**
1. Молоко (80.00₽, 50 шт)
2. Хлеб (30.00₽, 100 шт)
3. Яблоки (120.00₽, 30 шт)
4. Сыр (150.00₽, 20 шт)
5. Кефир (70.00₽, 40 шт)

**Заказы:**
1. Заказ #1: новый (без курьера)
2. Заказ #2: в доставке (с курьером vova)

## 🚀 Быстрый старт

```bash
# 1. Войти в папку
cd BackEnd

# 2. Запустить сервер
python manage.py runserver

# 3. Открыть в браузере
http://localhost:8000/api/products/
```

## 📚 Документация

- **QUICKSTART.md** — быстрый старт (начните отсюда!)
- **README.md** — полная документация проекта
- **TESTING.md** — примеры тестирования API
- **PROJECT_STRUCTURE.md** — детальное описание структуры

## 💡 Ключевые особенности реализации

1. **Авторизация через сессии** — используется встроенная в Django SessionAuthentication
2. **Хеширование паролей** — используется `make_password()` и `check_password()`
3. **Ролевая фильтрация** — заказы фильтруются в зависимости от роли пользователя
4. **Правильные отношения между моделями** — ForeignKey, OneToOne, CASCADE, PROTECT
5. **REST API** — правильные HTTP методы и статус-коды
6. **Django Admin** — все модели зарегистрированы и готовы к использованию
7. **Миграции** — правильная история изменений БД
8. **Локализация** — русский язык и московская временная зона

## 🔒 Безопасность

- ✓ Пароли хешируются при сохранении
- ✓ Сессии управляются Django
- ✓ CSRF защита в Django settings
- ✓ Permission classes для защиты эндпоинтов
- ✓ HTTPS готов для production

## ⚠️ Ограничения (как и требовалось)

- Только базовые возможности Django и DRF
- Нет JWT или токен-аутентификации
- Нет создания заказов через API (только чтение)
- Нет сложных бизнес-логик
- Нет внешних зависимостей кроме Django и DRF

## 🎓 Что можно изучить на этом проекте

1. **Django основы**: модели, миграции, админ-панель
2. **Django REST Framework**: views, serializers, permissions
3. **Авторизация**: сессии, базовая аутентификация
4. **API проектирование**: REST принципы, правильные HTTP методы
5. **База данных**: отношения, индексы, оптимизация запросов
6. **Тестирование**: API testing с curl, Postman, Python requests

## 📊 Статистика проекта

- **Приложений**: 3
- **Моделей**: 6
- **Views**: 6
- **Сериализаторов**: 3
- **URL patterns**: 6
- **Миграций**: 3
- **Строк кода**: ~500 (без комментариев)
- **Тестовых данных**: 2 пользователя, 5 товаров, 2 заказа

## ✨ Что было создано

1. ✅ Структура Django проекта
2. ✅ 3 приложения с моделями
3. ✅ REST API эндпоинты
4. ✅ Авторизация через сессии
5. ✅ Django миграции
6. ✅ Тестовые данные
7. ✅ Django Admin конфигурация
8. ✅ Подробная документация (4 файла)
9. ✅ Примеры использования API

## 🎉 Проект готов к использованию!

Все файлы созданы, миграции применены, тестовые данные загружены.

**Следующий шаг**: запустить сервер и протестировать API:

```bash
python manage.py runserver
curl http://localhost:8000/api/products/
```

---

Создано: 12 апреля 2026 года
Версия Django: 6.0.4
Версия DRF: 3.17.1
