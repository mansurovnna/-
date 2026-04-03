#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Product

# Маппинг старых названий на новые
rename_map = {
    'Black Dress': 'Чёрное платье',
    'Summer Dress': 'Летнее платье',
    'Casual Shirt': 'Повседневная рубашка',
    'Jeans': 'Джинсы',
    'Winter Coat': 'Зимнее пальто',
    'T-shirt': 'Футболка',
}

for old_name, new_name in rename_map.items():
    product = Product.objects.get(name=old_name)
    product.name = new_name
    product.save()
    print(f'✓ {old_name} → {new_name}')

print('\nВсе товары переименованы!')
