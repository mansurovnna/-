#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Category, Product

# Удалить ошибочно созданный товар iPhone 15
try:
    product = Product.objects.get(name='iPhone 15')
    product.delete()
    print('✓ Удален товар iPhone 15')
except Product.DoesNotExist:
    print('Товар iPhone 15 не найден')

# Удалить ошибочно созданную категорию Смартфоны
try:
    category = Category.objects.get(name='Смартфоны')
    if category.products.count() == 0:
        category.delete()
        print('✓ Удалена категория Смартфоны')
    else:
        print('В категории есть товары, не удаляю')
except Category.DoesNotExist:
    print('Категория Смартфоны не найдена')
