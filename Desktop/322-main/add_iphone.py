#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Category, Product, ProductImage
from decimal import Decimal
from django.core.files.base import ContentFile
import requests

# Получить или создать категорию "Телефоны"
category, created = Category.objects.get_or_create(
    slug='smartphones',
    defaults={'name': 'Смартфоны'}
)
if created:
    print(f'✓ Создана категория: {category.name}')

# Получить или создать товар iPhone
product, created = Product.objects.get_or_create(
    slug='iphone-15',
    defaults={
        'category': category,
        'name': 'iPhone 15',
        'description': 'Новейший смартфон Apple с современным дизайном и мощным процессором',
        'price': Decimal('150000'),
        'old_price': Decimal('180000'),
        'stock': 5,
        'is_active': True
    }
)
if created:
    print(f'✓ Создан товар: {product.name}')
else:
    print(f'Товар уже существует: {product.name}')

# URL картинки
image_url = 'https://prod-cdn.prod.asbis.io/s3size/el:t/f:webp/rt:fill/w:900/plain/s3://cms/product/2d/22/2d22e5e521d6491cf0dd8c0c8a47f2eb/250915140013863146.webp'

# Проверить, есть ли уже изображение
existing_image = ProductImage.objects.filter(product=product, image__contains='iphone').first()
if not existing_image:
    try:
        # Скачать изображение
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            # Создать изображение в БД
            image = ProductImage(
                product=product,
                alt_text='iPhone 15',
                is_main=True
            )
            
            # Сохранить картинку с именем
            filename = 'iphone-15.webp'
            image.image.save(
                f'products/{filename}',
                ContentFile(response.content),
                save=True
            )
            print(f'✓ Добавлено изображение к товару: {product.name}')
        else:
            print(f'✗ Ошибка при загрузке изображения: {response.status_code}')
    except Exception as e:
        print(f'✗ Ошибка: {str(e)}')
        print(f'  (Картинка будет загружена вручную через админку)')
else:
    print(f'Изображение уже есть у товара')

print(f'\nВсего товаров в категории "{category.name}": {category.products.count()}')
print(f'Всего изображений у товара "{product.name}": {product.images.count()}')
