#!/bin/bash

# Script для тестирования API endpoints
# Убедитесь, что сервер запущен: python manage.py runserver

BASE_URL="http://localhost:8000/api"

echo "=== Testing Delivery API ==="
echo ""

# Test 1: Get products
echo "1. GET /api/products/ - Получить список товаров"
curl -s -X GET "${BASE_URL}/products/" | python -m json.tool
echo ""

# Test 2: Get product detail
echo "2. GET /api/products/1/ - Получить информацию о товаре"
curl -s -X GET "${BASE_URL}/products/1/" | python -m json.tool
echo ""

# Test 3: Login
echo "3. POST /api/login/ - Вход (клиент ivan:password123)"
COOKIE=$(curl -s -c - -X POST "${BASE_URL}/login/" \
  -H "Content-Type: application/json" \
  -d '{"login": "ivan", "password": "password123"}' | \
  grep sessionid | awk '{print $7}')

echo "Session cookie: $COOKIE"
curl -s -b "sessionid=$COOKIE" -X POST "${BASE_URL}/login/" \
  -H "Content-Type: application/json" \
  -d '{"login": "ivan", "password": "password123"}' | python -m json.tool
echo ""

# Test 4: Get orders (authenticated)
echo "4. GET /api/orders/ - Получить заказы через curl (требует сессии)"
echo "Запустите это в новом терминале после логина:"
echo "curl -b 'sessionid=YOUR_SESSION_ID' http://localhost:8000/api/orders/"
echo ""

# Test 5: Logout
echo "5. POST /api/logout/ - Выход из системы"
echo "curl -X POST http://localhost:8000/api/logout/"
echo ""

echo "=== Для полного тестирования используйте Python скрипт ==="
echo ""
