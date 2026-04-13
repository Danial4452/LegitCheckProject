# Быстрый старт — Django Delivery App

## 📋 Что было создано

Полнофункциональное Django REST API приложение доставки товаров с авторизацией через сессии.

### ✅ Что реализовано:

- ✓ 3 приложения Django: `accounts`, `products`, `orders`
- ✓ 6 моделей базы данных с правильными связями
- ✓ REST API с 6 основными эндпоинтами
- ✓ Авторизация через SessionAuthentication (встроенные сессии Django)
- ✓ Ролевая модель: client, courier, support
- ✓ Фильтрация заказов по ролям
- ✓ Django Admin с регистрацией всех моделей
- ✓ Тестовые данные (5 товаров, 2 пользователя, 2 заказа)

## 🚀 Первый запуск

### 1. Проверить установку

```bash
cd "D:\Desktop\Subjects\Web Dev\GroupProj\LegitCheckProject\BackEnd"
python --version  # Должно быть 3.7+
pip list | findstr django  # Должно быть Django 6.0.4
```

### 2. Запустить сервер

```bash
python manage.py runserver
```

**Результат:**
```
Starting development server at http://127.0.0.1:8000/
```

### 3. Открыть в браузере

- **API**: http://localhost:8000/api/products/
- **Admin**: http://localhost:8000/admin/

## 🔐 Тестирование вхождения

### Через curl (PowerShell):

```powershell
# 1. Получить список товаров
curl -Uri "http://localhost:8000/api/products/" -Method GET

# 2. Войти как клиент
$response = curl -Uri "http://localhost:8000/api/login/" -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"login":"ivan","password":"password123"}' `
  -SessionVariable session

# 3. Получить заказы (с сохраненной сессией)
curl -Uri "http://localhost:8000/api/orders/" -Method GET -WebSession $session
```

### Через Python:

```python
import requests

session = requests.Session()

# Вход
r = session.post('http://localhost:8000/api/login/', json={
    'login': 'ivan',
    'password': 'password123'
})
print(r.json())  # {'message': 'ok', 'role': 'client'}

# Получить заказы
r = session.get('http://localhost:8000/api/orders/')
print(r.json())  # Список заказов клиента
```

## 📚 API Endpoints

| Метод | URL | Описание | Auth |
|-------|-----|---------|------|
| POST | `/api/login/` | Вход в систему | ✗ |
| POST | `/api/logout/` | Выход из системы | ✗ |
| GET | `/api/products/` | Список товаров | ✗ |
| GET | `/api/products/<id>/` | Информация о товаре | ✗ |
| GET | `/api/orders/` | Заказы (по ролям) | ✓ |
| POST | `/api/orders/<id>/cancel/` | Отменить заказ (только support) | ✓ |

## 👥 Тестовые пользователи

```
Клиент:
  login: ivan
  password: password123
  role: client

Курьер:
  login: vova
  password: password123
  role: courier
```

## 📁 Файлы проекта

```
BackEnd/
├── manage.py ........................ Django управление
├── db.sqlite3 ....................... База данных
├── requirements.txt ................. Зависимости
├── README.md ........................ Основная документация
├── TESTING.md ....................... Руководство по тестированию
├── PROJECT_STRUCTURE.md ............ Подробная структура
├── QUICKSTART.md (этот файл)
├── sample_usage.py .................. Создание тестовых данных
├── test_api.sh ...................... Bash скрипт для тестирования
│
├── config/ .......................... Конфиг проекта
│   ├── settings.py ................. Основные настройки ⭐
│   ├── urls.py ..................... Главные URL ⭐
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/ ........................ Авторизация
│   ├── models.py (Role, User, Profile) ⭐
│   ├── views.py (LoginView, LogoutView) ⭐
│   ├── admin.py .................... Django Admin
│   ├── urls.py
│   └── management/commands/
│       └── initialize_data.py ...... Инициализация ролей
│
├── products/ ........................ Товары
│   ├── models.py (Product) ⭐
│   ├── views.py ⭐
│   ├── serializers.py ⭐
│   ├── urls.py
│   └── admin.py
│
└── orders/ .......................... Заказы
    ├── models.py (Order, OrderItem, OrderStatus) ⭐
    ├── views.py (OrderListView, OrderCancelView) ⭐
    ├── serializers.py ⭐
    ├── urls.py
    └── admin.py
```

⭐ = Основные файлы для расширения

## 🛠️ Полезные команды

```bash
# Запустить сервер
python manage.py runserver

# Запустить сервер на другом порту
python manage.py runserver 8080

# Создать суперпользователя для админки
python manage.py createsuperuser

# Django интерактивный shell
python manage.py shell

# Создать резервную копию БД
python manage.py dumpdata > backup.json

# Восстановить БД из резервной копии
python manage.py loaddata backup.json

# Очистить БД и пересоздать
rm db.sqlite3
python manage.py migrate
python manage.py initialize_data
python sample_usage.py
```

## 🧪 Примеры API запросов

### Получить товары
```bash
curl http://localhost:8000/api/products/
```

### Войти
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"login":"ivan","password":"password123"}' \
  -c cookies.txt
```

### Получить заказы (с сохраненными куками)
```bash
curl http://localhost:8000/api/orders/ -b cookies.txt
```

### Выход
```bash
curl -X POST http://localhost:8000/api/logout/ \
  -b cookies.txt
```

## 🔍 Проверка наличия данных

```python
python manage.py shell

# Проверить роли
from accounts.models import Role
Role.objects.all()  # Должны быть: client, courier, support

# Проверить пользователей
from accounts.models import User
User.objects.all()  # Должны быть: ivan, vova

# Проверить товары
from products.models import Product
Product.objects.count()  # Должно быть 5

# Проверить заказы
from orders.models import Order
Order.objects.count()  # Должно быть 2

# Проверить статусы
from orders.models import OrderStatus
OrderStatus.objects.values_list('name', flat=True)  # new, accepted, в_доставке, доставлено, отменено
```

## 🐛 Решение проблем

### Ошибка: port 8000 already in use

```bash
# Найти процесс, использующий порт
netstat -ano | findstr :8000

# Запустить на другом порту
python manage.py runserver 8080
```

### Ошибка: no such table

```bash
# Применить миграции
python manage.py migrate
```

### Ошибка: ModuleNotFoundError

```bash
# Переустановить зависимости
pip install -r requirements.txt
```

### Сбросить БД полностью

```bash
# Удалить файл базы данных
rm db.sqlite3

# Пересоздать
python manage.py migrate
python manage.py initialize_data
python sample_usage.py
```

## 📖 Больше информации

- **Подробная документация**: см. [README.md](README.md)
- **Тестирование API**: см. [TESTING.md](TESTING.md)
- **Структура проекта**: см. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 🎓 Обучающие материалы

### Изучение Django

1. Официальная документация: https://docs.djangoproject.com/
2. Django для начинающих: https://djangoforbeginners.com/

### Изучение DRF

1. Официальная документация: https://www.django-rest-framework.org/
2. REST API концепции: https://restfulapi.net/

## 🚀 Следующие шаги

1. ✅ Запустить сервер и протестировать API
2. 📖 Прочитать документацию в README.md
3. 🧪 Попробовать примеры в TESTING.md
4. 💡 Добавить новые функции (см. PROJECT_STRUCTURE.md)
5. 🔒 Изучить код моделей и представлений

---

**Сервер готов к работе! Удачи с разработкой! 🎉**
