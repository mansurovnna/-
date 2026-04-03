# Переменные окружения (Environment Variables)

В этом проекте используется файл `.env` для управления конфигурацией через переменные окружения. Это позволяет:

✅ Хранить чувствительные данные (пароли, ключи) вне исходного кода  
✅ Легко переключаться между разработкой и production  
✅ Не коммитить конфиденциальную информацию на GitHub  

## Установка python-decouple

```bash
pip install python-decouple
```

## Переменные окружения

### Django настройки

| Переменная | Описание | По умолчанию |
|-----------|---------|-------------|
| `DEBUG` | Режим отладки (True/False) | `True` |
| `SECRET_KEY` | Секретный ключ Django | `django-insecure-...` |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `localhost,127.0.0.1` |

### База данных

| Переменная | Описание | По умолчанию |
|-----------|---------|-------------|
| `DATABASE_ENGINE` | Движок БД | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Имя БД или путь | `db.sqlite3` |
| `DATABASE_USER` | Пользователь БД | (пусто) |
| `DATABASE_PASSWORD` | Пароль БД | (пусто) |
| `DATABASE_HOST` | Хост БД | (пусто) |
| `DATABASE_PORT` | Порт БД | (пусто) |

### Интернационализация

| Переменная | Описание | По умолчанию |
|-----------|---------|-------------|
| `LANGUAGE_CODE` | Код языка | `ru` |
| `TIME_ZONE` | Часовой пояс | `Europe/Moscow` |

## Файлы

### `.env` (для разработки)
Локальный файл с вашими переменными окружения. **НЕ коммитится на GitHub** (.env в .gitignore).

### `.env.example`
Пример файла с описанием всех переменных. Коммитится на GitHub. Разработчики копируют его в .env и заполняют свои значения.

## Как использовать

### Для разработки

1. Скопируйте `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```

2. Отредактируйте значения в `.env` под вашу локальную систему

3. Всё! Код автоматически будет читать значения из `.env`

### Для production

1. На сервере создайте `.env` файл с production-значениями:
   ```bash
   DEBUG=False
   SECRET_KEY=your-very-secret-key-here
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=shop_db
   DATABASE_USER=postgres
   DATABASE_PASSWORD=very-secure-password
   DATABASE_HOST=database.example.com
   DATABASE_PORT=5432
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите миграции:
   ```bash
   python manage.py migrate
   ```

## Примеры конфигурации

### Разработка (SQLite)
```env
DEBUG=True
SECRET_KEY=dev-key-123
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

### Production (PostgreSQL)
```env
DEBUG=False
SECRET_KEY=super-secret-production-key
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=shop_prod
DATABASE_USER=postgres
DATABASE_PASSWORD=secure-password
DATABASE_HOST=db.example.com
DATABASE_PORT=5432
```

## Безопасность

⚠️ **НИКОГДА** не коммитьте `.env` файл на GitHub!

✅ Пример безопасного workflow:
```bash
git add settings.py forms.py  # Коммитим код
git add .env.example          # Коммитим шаблон
git status                     # .env должен быть в "Untracked files"
# .env автоматически в .gitignore, так что git его не затронет
```