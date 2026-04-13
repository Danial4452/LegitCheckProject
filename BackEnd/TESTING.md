# API Testing Guide

Руководство для тестирования REST API приложения доставки.

## Установка инструментов

### Вариант 1: curl (встроен в Windows 10+)

Не требует установки, доступен в PowerShell или CMD.

### Вариант 2: Postman (GUI)

Скачать с https://www.postman.com/downloads/

### Вариант 3: Python requests

```bash
pip install requests
```

## Запуск сервера

```bash
cd BackEnd
python manage.py runserver
```

Сервер будет доступен на `http://localhost:8000/`

## Тестовые учетные данные

После запуска `python sample_usage.py` доступны:

**Клиент:**
- Логин: `ivan`
- Пароль: `password123`
- Роль: `client`

**Курьер:**
- Логин: `vova`
- Пароль: `password123`
- Роль: `courier`

## Примеры запросов

### 1. Получить список товаров

**GET** `/api/products/`

```bash
curl -X GET http://localhost:8000/api/products/
```

**Ответ (200):**
```json
[
    {
        "id": 1,
        "name": "Молоко",
        "description": "Свежее коровье молоко 1л",
        "price": "80.00",
        "stock": 50,
        "is_available": true
    },
    {
        "id": 2,
        "name": "Хлеб",
        "description": "Белый хлеб",
        "price": "30.00",
        "stock": 100,
        "is_available": true
    }
]
```

### 2. Получить информацию об одном товаре

**GET** `/api/products/1/`

```bash
curl -X GET http://localhost:8000/api/products/1/
```

**Ответ (200):**
```json
{
    "id": 1,
    "name": "Молоко",
    "description": "Свежее коровье молоко 1л",
    "price": "80.00",
    "stock": 50,
    "is_available": true
}
```

### 3. Вход в систему (Login)

**POST** `/api/login/`

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "login": "ivan",
    "password": "password123"
  }' \
  -c cookies.txt
```

Флаг `-c cookies.txt` сохраняет куки в файл.

**Ответ (200):**
```json
{
    "message": "ok",
    "role": "client"
}
```

**Ошибка (400):**
```json
{
    "error": "Неверный логин или пароль"
}
```

### 4. Получить список заказов (выполнить после логина)

**GET** `/api/orders/`

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -b cookies.txt
```

Флаг `-b cookies.txt` использует сохраненные куки.

**Ответ для клиента (200):**
```json
[
    {
        "id": 1,
        "client": 1,
        "client_login": "ivan",
        "courier": null,
        "courier_login": null,
        "status": 1,
        "status_name": "new",
        "address": "Москва, ул. Примерная, 123",
        "note": "Позвонить перед приездом",
        "total_price": "230.00",
        "created_at": "2024-04-12T10:30:00Z",
        "updated_at": "2024-04-12T10:30:00Z",
        "items": [
            {
                "id": 1,
                "product": 1,
                "product_name": "Молоко",
                "quantity": 2,
                "price": "80.00"
            }
        ]
    }
]
```

### 5. Курьер пытается получить заказы

**Последовательность команд:**

```bash
# 1. Логин курьера
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "login": "vova",
    "password": "password123"
  }' \
  -c courier_cookies.txt

# 2. Получить свободные заказы и принятые им
curl -X GET http://localhost:8000/api/orders/ \
  -b courier_cookies.txt
```

**Ответ для курьера:**
```json
[
    {
        "id": 1,
        "client": 1,
        "client_login": "ivan",
        "courier": null,
        "courier_login": null,
        "status": 1,
        "status_name": "new",
        ...
    },
    {
        "id": 2,
        "client": 1,
        "client_login": "ivan",
        "courier": 2,
        "courier_login": "vova",
        "status": 3,
        "status_name": "in_delivery",
        ...
    }
]
```

### 6. Отменить заказ (только для support)

**POST** `/api/orders/1/cancel/`

```bash
# Сначала логин как support пользователь
# (примечание: support пользователя еще нет, создайте через Django shell)

curl -X POST http://localhost:8000/api/orders/1/cancel/ \
  -b cookies.txt
```

**Ответ (200):**
```json
{
    "message": "Заказ отменён"
}
```

**Ошибка (403) - не является support:**
```json
{
    "error": "Только support может отменять заказы"
}
```

### 7. Выход из системы (Logout)

**POST** `/api/logout/`

```bash
curl -X POST http://localhost:8000/api/logout/ \
  -b cookies.txt
```

**Ответ (200):**
```json
{
    "message": "Вышли из системы"
}
```

## Тестирование ошибок

### Попытка получить заказы без авторизации

```bash
curl -X GET http://localhost:8000/api/orders/
```

**Ответ (401):**
```json
{
    "error": "Не авторизованы"
}
```

### Попытка отменить чужой заказ

```bash
# Логин как клиент
curl -b cookies.txt -X POST http://localhost:8000/api/orders/1/cancel/
```

**Ответ (403):**
```json
{
    "error": "Только support может отменять заказы"
}
```

## Полный сценарий тестирования

### Сценарий 1: Клиент просматривает товары и заказы

```bash
# 1. Просмотр товаров (без авторизации)
curl -X GET http://localhost:8000/api/products/

# 2. Вход
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"login":"ivan","password":"password123"}' \
  -c client.txt

# 3. Просмотр своих заказов
curl -X GET http://localhost:8000/api/orders/ -b client.txt

# 4. Выход
curl -X POST http://localhost:8000/api/logout/ -b client.txt
```

### Сценарий 2: Курьер ищет заказы на доставку

```bash
# 1. Логин курьера
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"login":"vova","password":"password123"}' \
  -c courier.txt

# 2. Просмотр доступных заказов
curl -X GET http://localhost:8000/api/orders/ -b courier.txt

# 3. Просмотр конкретного товара
curl -X GET http://localhost:8000/api/products/1/

# 4. Выход
curl -X POST http://localhost:8000/api/logout/ -b courier.txt
```

## Windows PowerShell примеры

В PowerShell используются немного другие флаги для curl:

```powershell
# Получить товары
curl -Uri "http://localhost:8000/api/products/" -Method GET

# Логин
$response = curl -Uri "http://localhost:8000/api/login/" -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"login":"ivan","password":"password123"}' `
  -SessionVariable session

# Использовать сессию для последующих запросов
curl -Uri "http://localhost:8000/api/orders/" -Method GET -WebSession $session
```

## Отладка

### Проверить сессию в браузере

1. Откройте DevTools (F12)
2. Перейдите на вкладку Application/Storage
3. Найдите Cookies для localhost:8000
4. Проверьте наличие sessionid

### Просмотр логов сервера

Логи Django выводятся в консоль, где запущен `runserver`.

Ищите:
- `"POST /api/login/ HTTP/1.1" 200`
- `"GET /api/orders/ HTTP/1.1" 200`
- Ошибки с кодами 400, 403, 404, 500

## Создание support пользователя для тестирования

```bash
python manage.py shell
```

Затем в Python shell:

```python
from accounts.models import User, Role

support_role = Role.objects.get(name='support')
support_user = User(login='admin', role=support_role)
support_user.set_password('admin123')
support_user.save()

print(f"Создан support пользователь: admin (пароль: admin123)")
```

Выход из shell: `exit()`

## Дополнительные команды

### Сбросить базу данных

```bash
# Удалить db.sqlite3
rm db.sqlite3

# Заново создать базу
python manage.py migrate
python manage.py initialize_data
python sample_usage.py
```

### Просмотр истории заказов в админке

```
http://localhost:8000/admin/
```

Логин: admin (если суперпользователь был создан)
