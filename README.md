

````markdown
# mini-app-tg-shop

**Мини-магазин, реализованный на Django с использованием шаблонов, предназначенный для интерфейса мини-приложений Telegram.**

Особенности проекта:  
- Возможность перейти в чат с продавцом, где автоматически подставляется текст с описанием интересующего товара.  
- Использование модуля `django-mptt` для организации иерархии категорий и оптимизации запросов к базе данных.  
- В `master` ветке есть готовый `docker-compose.yml`, который запускает 3 сервиса:  
  - `web` — Django-приложение  
  - `postgres` — сервер базы данных PostgreSQL  
  - `nginx` — веб-сервер

---

## Быстрый старт

1. Клонируйте ветку `master`:  
   ```bash
   git clone -b master <URL_репозитория>
   cd mini-app-tg-shop
````

2. Создайте файл `.env` с обязательными переменными окружения:

   ```env
   DJANGO_SECRET_KEY="django-insecure-4v1j3!@#&*^%$#@!"
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,[::1]

   POSTGRES_USER=django_user        # Имя пользователя для PostgreSQL
   POSTGRES_PASSWORD=1234           # Пароль для PostgreSQL
   POSTGRES_DB=django_db            # Имя базы данных
   DB_HOST=postgres                 # Имя сервиса/контейнера базы данных (не менять)
   DB_PORT=5432                    # Порт базы данных
   ```

3. Запустите контейнеры и соберите проект:

   ```bash
   docker compose up --build
   ```

4. После запуска контейнеров выполните миграции и соберите статические файлы:

   ```bash
   docker compose exec web sh
   python manage.py migrate
   python manage.py collectstatic --noinput
   exit
   ```

---

## Дополнительно

* Для доступа в shell контейнера Django используйте:

  ```bash
  docker compose exec web sh
  ```

---

## Структура проекта (кратко)

* `shop_tg_app/` — исходники Django-приложения
* `postgres/` — данные и конфигурация PostgreSQL
* `nginx/` — конфигурация веб-сервера nginx

---

