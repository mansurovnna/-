#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Product, ProductImage
from django.core.files.base import ContentFile
import requests

# Найти товар iPhone в категории Телефоны
try:
    product = Product.objects.get(name='iPhone')
    print(f'Найден товар: {product.name}')
except Product.DoesNotExist:
    print('Товар iPhone не найден')
    exit()

# URL картинки
image_url = 'https://prod-cdn.prod.asbis.io/s3size/el:t/f:webp/rt:fill/w:900/plain/s3://cms/product/2d/22/2d22e5e521d6491cf0dd8c0c8a47f2eb/250915140013863146.webp'

try:
    # Скачать изображение
    response = requests.get(image_url, timeout=10)
    if response.status_code == 200:
        # Создать изображение в БД
        image = ProductImage(
            product=product,
            alt_text='iPhone',
            is_main=True
        )
        
        # Сохранить картинку с именем
        filename = 'iphone.webp'
        image.image.save(
            f'products/{filename}',
            ContentFile(response.content),
            save=True
        )
        print(f'✓ Добавлено изображение к товару: {product.name}')
        print(f'✓ Всего изображений: {product.images.count()}')
    else:
        print(f'✗ Ошибка при загрузке изображения: {response.status_code}')
except Exception as e:
    print(f'✗ Ошибка: {str(e)}')
