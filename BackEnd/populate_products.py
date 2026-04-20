import os
import django
import sqlite3

# 1. Alter table
db_path = 'db.sqlite3'
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('ALTER TABLE products_product ADD COLUMN brand varchar(100) DEFAULT "Unknown"')
    c.execute('ALTER TABLE products_product ADD COLUMN is_authentic bool DEFAULT 1')
    c.execute('ALTER TABLE products_product ADD COLUMN serial_number varchar(100) DEFAULT "TEMP"')
    c.execute('ALTER TABLE products_product ADD COLUMN manufacture_location varchar(255) DEFAULT ""')
    c.execute('ALTER TABLE products_product ADD COLUMN history text DEFAULT ""')
    c.execute('ALTER TABLE products_product ADD COLUMN image_url varchar(200)')
    conn.commit()
    conn.close()
    print("Table altered successfully.")
except Exception as e:
    print("Alter table skipped or failed:", e)

# 2. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from accounts.models import User, Role

# Make sure we have a user
role, _ = Role.objects.get_or_create(name='Expert')
user, _ = User.objects.get_or_create(login='admin', defaults={'password': '123', 'role': role})

# 3. Populate products
products_data = [
    {"name": "Air Jordan 1 Retro High", "brand": "Nike", "is_authentic": True, "serial_number": "AJ1-RETRO-001", "manufacture_location": "Vietnam", "history": "Purchased from official store", "price": 199.99},
    {"name": "Yeezy Boost 350 V2", "brand": "Adidas", "is_authentic": True, "serial_number": "YZY-350-002", "manufacture_location": "China", "history": "StockX verified", "price": 299.99},
    {"name": "Off-White x Nike Air Presto", "brand": "Nike", "is_authentic": False, "serial_number": "OW-PRST-FAKE1", "manufacture_location": "Unknown", "history": "Suspicious seller on local market", "price": 50.00},
    {"name": "Supreme Box Logo Hoodie", "brand": "Supreme", "is_authentic": True, "serial_number": "SUP-BOGO-004", "manufacture_location": "Canada", "history": "Retail drop", "price": 400.00},
    {"name": "Gucci Ace Sneakers", "brand": "Gucci", "is_authentic": True, "serial_number": "GUC-ACE-005", "manufacture_location": "Italy", "history": "Gucci boutique Paris", "price": 650.00},
    {"name": "Balenciaga Triple S", "brand": "Balenciaga", "is_authentic": False, "serial_number": "BAL-TRP-FAKE2", "manufacture_location": "Unknown", "history": "Gift from a friend, materials feel off", "price": 120.00},
    {"name": "Nike Dunk Low Panda", "brand": "Nike", "is_authentic": True, "serial_number": "DUNK-PND-007", "manufacture_location": "Indonesia", "history": "SNKRS app win", "price": 110.00},
    {"name": "Rolex Submariner", "brand": "Rolex", "is_authentic": True, "serial_number": "ROL-SUB-008", "manufacture_location": "Switzerland", "history": "Authorized dealer", "price": 10000.00},
    {"name": "Louis Vuitton Keepall", "brand": "Louis Vuitton", "is_authentic": False, "serial_number": "LV-KPLL-FAKE3", "manufacture_location": "Unknown", "history": "Thrift store find, bad stitching", "price": 80.00},
    {"name": "Travis Scott x Air Jordan 4", "brand": "Nike", "is_authentic": True, "serial_number": "TS-AJ4-010", "manufacture_location": "China", "history": "FlightClub purchase", "price": 800.00},
]

from orders.models import OrderItem, Order

OrderItem.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete() # Clear old ones to prevent unique constraint issues
for p in products_data:
    Product.objects.create(**p, owner=user)

print("Added 10 products successfully!")
