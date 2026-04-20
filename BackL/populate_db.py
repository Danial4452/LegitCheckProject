import os
import django
import random
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackL.settings')
django.setup()

from django.contrib.auth.models import User
from Category.models import Category
from Product.models import Product

def generate_products():
    print("Создаем пользователя и категории...")
    owner, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@test.com'})
    owner.set_password('admin123')
    owner.save()

    categories_data = ['Кроссовки', 'Сумки', 'Часы', 'Одежда', 'Аксессуары']
    categories = {}
    for c_name in categories_data:
        cat, _ = Category.objects.get_or_create(name=c_name)
        categories[c_name] = cat

    # Наборы реалистичных данных с префиксами
    # Формат: (Brand, Name, Category, Location, Prefix)
    sneakers = [
        ('Nike', 'Air Jordan 1 Retro High Chicago', 'Кроссовки', 'China', 'AJ1-RETRO'),
        ('Nike', 'Dunk Low Panda', 'Кроссовки', 'Vietnam', 'DUNK-PND'),
        ('adidas', 'Yeezy Boost 350 V2 Zebra', 'Кроссовки', 'Vietnam', 'YZY-350'),
        ('New Balance', '990v5 Grey', 'Кроссовки', 'USA', 'NB-990'),
        ('Nike', 'Air Max 95 OG Neon', 'Кроссовки', 'Indonesia', 'AM95-OG'),
        ('Balenciaga', 'Triple S', 'Кроссовки', 'China', 'BAL-TRP'),
        ('Travis Scott x Nike', 'Air Jordan 1 Low Reverse Mocha', 'Кроссовки', 'China', 'TS-AJ1'),
        ('Nike', 'Air Jordan 4 Retro', 'Кроссовки', 'China', 'TS-AJ4'),
    ]

    watches = [
        ('Rolex', 'Submariner Date 116610LN', 'Часы', 'Switzerland', 'ROL-SUB'),
        ('Omega', 'Speedmaster Moonwatch', 'Часы', 'Switzerland', 'OMG-SPD'),
        ('Patek Philippe', 'Nautilus 5711/1A', 'Часы', 'Switzerland', 'PP-NAU'),
        ('Audemars Piguet', 'Royal Oak 15400ST', 'Часы', 'Switzerland', 'AP-RO'),
        ('Tag Heuer', 'Carrera Chronograph', 'Часы', 'Switzerland', 'TAG-CAR'),
    ]

    bags = [
        ('Louis Vuitton', 'Neverfull MM Monogram', 'Сумки', 'France', 'LV-NVF'),
        ('Gucci', 'GG Marmont Matelassé Mini', 'Сумки', 'Italy', 'GUC-MAR'),
        ('Chanel', 'Classic Double Flap Bag', 'Сумки', 'France', 'CHN-CF'),
        ('Hermès', 'Birkin 30 Togo Leather', 'Сумки', 'France', 'HER-BIR'),
        ('Prada', 'Re-Edition 2005 Nylon Bag', 'Сумки', 'Italy', 'PRA-RE'),
        ('Louis Vuitton', 'Keepall Bandouliere', 'Сумки', 'France', 'LV-KPLL'),
    ]

    clothing = [
        ('Supreme', 'Box Logo Hoodie', 'Одежда', 'Canada', 'SUP-BOGO'),
        ('BAPE', 'Shark Full Zip Hoodie', 'Одежда', 'Japan', 'BAPE-SHK'),
        ('Off-White', 'Diagonal Arrows T-Shirt', 'Одежда', 'Portugal', 'OW-ARR'),
        ('Off-White', 'Presto White', 'Одежда', 'Portugal', 'OW-PRST'),
        ('Gucci', 'Vintage Logo T-Shirt', 'Одежда', 'Italy', 'GUC-VINT'),
        ('Gucci', 'Ace Sneakers', 'Одежда', 'Italy', 'GUC-ACE'),
        ('Stone Island', 'Crinkle Reps NY Down Jacket', 'Одежда', 'Romania', 'SI-CRNK'),
    ]

    accessories = [
        ('Chrome Hearts', 'Cemetery Ring', 'Аксессуары', 'USA', 'CH-CEM'),
        ('Louis Vuitton', 'Multiple Wallet Monogram', 'Аксессуары', 'France', 'LV-MUL'),
        ('Hermès', 'H Belt Reversible', 'Аксессуары', 'France', 'HER-HBLT'),
        ('Gucci', 'Double G Leather Belt', 'Аксессуары', 'Italy', 'GUC-DBLG'),
    ]

    all_templates = sneakers * 3 + watches * 3 + bags * 3 + clothing * 3 + accessories * 3
    random.shuffle(all_templates)

    print("Удаляем старые товары для чистоты...")
    Product.objects.all().delete()

    products_to_create = []

    legit_count = 1
    fake_count = 1
    global_index = 1

    # Генерируем 50 товаров вперемешку
    for i in range(50):
        template = all_templates[i % len(all_templates)]
        brand, name, cat_name, loc, prefix = template
        
        is_legit = i % 2 == 0  # чередуем 25 настоящих и 25 фейковых

        if is_legit:
            serial = f"{prefix}-{global_index:03d}"
            history = f"Приобретено в официальном бутике {brand} в {random.choice(['Лондоне', 'Нью-Йорке', 'Париже', 'Милане', 'Токио', 'Дубае'])}.\nВсе швы идеальные, серийный номер совпадает с сертификатом. Оригинальная коробка в наличии.\n100% Legit."
            p = Product(
                owner=owner,
                category=categories[cat_name],
                name=name,
                brand=brand,
                is_authentic=True,
                serial_number=serial,
                manufacture_location=loc,
                history=history,
                image_url=f"https://source.unsplash.com/800x600/?{cat_name},{brand.replace(' ', '')}"
            )
            global_index += 1
        else:
            serial = f"{prefix}-FAKE{fake_count}"
            flaw = random.choice([
                "Неровная строчка на логотипе",
                "Слишком резкий химический запах клея",
                "Неправильный шрифт на бирке размера",
                "Коробка сделана из тонкого картона, отличается цвет",
                "Серийный номер не пробивается по базе производителя",
                "Вес изделия заметно легче оригинала",
                "Дешевая фурнитура, молния заедает"
            ])
            history = f"Куплено с рук на реселл-платформе без чека.\nПри детальной проверке выявлено: {flaw}.\nВердикт: Качественная реплика (Fake)."
            fake_loc = random.choice(['China (Unlicensed Factory)', 'Unknown', loc])
            p = Product(
                owner=owner,
                category=categories[cat_name],
                name=name + " (Replica)",
                brand=brand,
                is_authentic=False,
                serial_number=serial,
                manufacture_location=fake_loc,
                history=history,
                image_url=f"https://source.unsplash.com/800x600/?{cat_name},{brand.replace(' ', '')}"
            )
            fake_count += 1
            global_index += 1

        products_to_create.append(p)

    Product.objects.bulk_create(products_to_create)
    print(f"Успешно добавлено {len(products_to_create)} товаров (25 Legit / 25 Fake)!")


if __name__ == '__main__':
    generate_products()
