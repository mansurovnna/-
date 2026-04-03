# Django Магазин

Интернет-магазин на Django с корзиной, заказами и аутентификацией пользователей.

## Запуск проекта

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Выполните миграции:
   ```bash
   python manage.py migrate
   ```

5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## Демо-данные

Для создания демо-данных запустите:
```bash
python create_test_products.py
```

## Тестовый пользователь

- Логин: testuser
- Пароль: testpass123

## Функционал

- Просмотр каталога товаров
- Поиск и фильтрация
- Корзина покупок
- Оформление заказов
- Регистрация и вход пользователей
- Личный кабинет с заказами
- Админ-панель для управления товарами и заказами

## Скриншоты

### Каталог товаров
![Каталог](screenshots/catalog.png)

### Корзина
![Корзина](screenshots/cart.png)

### Оформление заказа
![Заказ](screenshots/order.png)

### Мои заказы
![Заказы](screenshots/my_orders.png)