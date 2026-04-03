#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Category, Product, ProductImage
from decimal import Decimal

# Создание категорий
categories_data = [
    {'name': 'Одежда', 'slug': 'clothes'},
    {'name': 'Обувь', 'slug': 'shoes'},
    {'name': 'Аксессуары', 'slug': 'accessories'},
    {'name': 'Электроника', 'slug': 'electronics'},
    {'name': 'Книги', 'slug': 'books'},
]

for data in categories_data:
    category, created = Category.objects.get_or_create(**data)
    if created:
        print(f'✓ Создана категория: {category.name}')

# Получение категорий
clothes = Category.objects.get(slug='clothes')
shoes = Category.objects.get(slug='shoes')
accessories = Category.objects.get(slug='accessories')
electronics = Category.objects.get(slug='electronics')
books = Category.objects.get(slug='books')

# Создание товаров
products_data = [
    # Одежда
    {'category': clothes, 'name': 'Чёрное платье', 'slug': 'black-dress', 'description': 'Красивое чёрное платье для вечеринок', 'price': Decimal('15000'), 'old_price': Decimal('20000'), 'stock': 5},
    {'category': clothes, 'name': 'Летнее платье', 'slug': 'summer-dress', 'description': 'Лёгкое летнее платье с узором', 'price': Decimal('8500'), 'stock': 0},
    {'category': clothes, 'name': 'Повседневная рубашка', 'slug': 'casual-shirt', 'description': 'Удобная повседневная рубашка', 'price': Decimal('5500'), 'stock': 12},
    {'category': clothes, 'name': 'Джинсы', 'slug': 'jeans', 'description': 'Классические синие джинсы', 'price': Decimal('12000'), 'stock': 3},
    {'category': clothes, 'name': 'Зимнее пальто', 'slug': 'winter-coat', 'description': 'Тёплое зимнее пальто', 'price': Decimal('45000'), 'stock': 2},
    {'category': clothes, 'name': 'Футболка', 'slug': 't-shirt', 'description': 'Базовая футболка из хлопка', 'price': Decimal('3500'), 'stock': 20},
    {'category': clothes, 'name': 'Юбка', 'slug': 'skirt', 'description': 'Элегантная юбка', 'price': Decimal('8000'), 'stock': 8},
    {'category': clothes, 'name': 'Брюки', 'slug': 'pants', 'description': 'Классические брюки', 'price': Decimal('10000'), 'stock': 15},

    # Обувь
    {'category': shoes, 'name': 'Кроссовки Nike', 'slug': 'nike-sneakers', 'description': 'Спортивные кроссовки', 'price': Decimal('25000'), 'stock': 10},
    {'category': shoes, 'name': 'Туфли', 'slug': 'heels', 'description': 'Элегантные туфли на каблуке', 'price': Decimal('18000'), 'stock': 0},
    {'category': shoes, 'name': 'Ботинки', 'slug': 'boots', 'description': 'Кожаные ботинки', 'price': Decimal('30000'), 'stock': 6},
    {'category': shoes, 'name': 'Сандалии', 'slug': 'sandals', 'description': 'Летние сандалии', 'price': Decimal('5000'), 'stock': 12},

    # Аксессуары
    {'category': accessories, 'name': 'Сумка', 'slug': 'bag', 'description': 'Стильная сумка', 'price': Decimal('12000'), 'stock': 7},
    {'category': accessories, 'name': 'Шарф', 'slug': 'scarf', 'description': 'Шерстяной шарф', 'price': Decimal('3000'), 'stock': 20},
    {'category': accessories, 'name': 'Очки', 'slug': 'sunglasses', 'description': 'Солнцезащитные очки', 'price': Decimal('8000'), 'stock': 5},

    # Электроника
    {'category': electronics, 'name': 'Смартфон', 'slug': 'smartphone', 'description': 'Современный смартфон', 'price': Decimal('150000'), 'stock': 3},
    {'category': electronics, 'name': 'Наушники', 'slug': 'headphones', 'description': 'Беспроводные наушники', 'price': Decimal('25000'), 'stock': 8},
    {'category': electronics, 'name': 'Планшет', 'slug': 'tablet', 'description': 'Планшет для работы', 'price': Decimal('80000'), 'stock': 2},

    # Книги
    {'category': books, 'name': 'Python для начинающих', 'slug': 'python-book', 'description': 'Учебник по Python', 'price': Decimal('2500'), 'stock': 15},
    {'category': books, 'name': 'Django руководство', 'slug': 'django-book', 'description': 'Полное руководство по Django', 'price': Decimal('3500'), 'stock': 10},
]

for data in products_data:
    product, created = Product.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        print(f'✓ Создан товар: {product.name} ({product.price} тг, stock={product.stock})')

# Добавление фото к товарам
images_data = [
    {'product_slug': 'black-dress', 'image': 'products/product-a-1.jpg', 'is_main': True},
    {'product_slug': 'summer-dress', 'image': 'products/product-b-1.jpg', 'is_main': True},
    {'product_slug': 'casual-shirt', 'image': 'products/product-b-2.jpg', 'is_main': True},
    {'product_slug': 'jeans', 'image': 'products/product-b-3.jpg', 'is_main': True},
    {'product_slug': 'winter-coat', 'image': 'products/product-c-1.jpg', 'is_main': True},
    {'product_slug': 'nike-sneakers', 'image': 'products/product-a-1.jpg', 'is_main': True},
    {'product_slug': 'smartphone', 'image': 'products/product-b-1.jpg', 'is_main': True},
]

for data in images_data:
    try:
        product = Product.objects.get(slug=data['product_slug'])
        image, created = ProductImage.objects.get_or_create(
            product=product,
            image=data['image'],
            defaults={'is_main': data['is_main']}
        )
        if created:
            print(f'✓ Добавлено фото к товару: {product.name}')
    except Product.DoesNotExist:
        print(f'✗ Товар {data["product_slug"]} не найден')

print(f'\nВсего категорий: {Category.objects.count()}')
print(f'Всего товаров: {Product.objects.count()}')
print(f'Всего фото: {ProductImage.objects.count()}')
