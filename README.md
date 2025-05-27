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

## Скриншоты интерфейса 

<p align="center">
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/main_page.jpg" alt="Главная страница" width="250"/>
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/main_page_sortings.jpg" alt="Сортировки" width="250"/>
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/inspect_page.jpg" alt="Страница продукта" width="250"/>
</p>

## Быстрый старт

1. Клонируйте ветку `master`:  
   ```bash
   git clone -b master https://github.com/hurtki/shop-mini-app.git
   cd mini-app-tg-shop

# 2. Создайте файл `.env` с обязательными переменными окружения:

``` python
DJANGO_SECRET_KEY="your key" # секретный ключ django

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,[::1]

POSTGRES_USER=django_user        # Имя пользователя для PostgreSQL

POSTGRES_PASSWORD=1234           # Пароль для PostgreSQL

POSTGRES_DB=django_db            # Имя базы данных

DB_HOST=postgres                 # Имя сервиса/контейнера базы данных (не менять)

DB_PORT=5432                    # Порт базы данных
```

# 3.Запустите контейнеры и соберите проект:

 ```bash
 docker compose up --build
 ```

# 4. После запуска контейнеров выполните миграции и соберите статические файлы:

 ```bash
 docker exec -it --user root tg-shop-django sh
 # если не хватает прав на collectstatic
 python manage.py migrate
 python manage.py collectstatic --noinput
 exit
 ```


## Дополнительно

* Для доступа в shell контейнера Django используйте:

  ```bash
  docker exec -it --user root tg-shop-django sh
  ```

---

## Структура проекта (кратко)

* `shop_tg_app/` — исходники Django-приложения
* `nginx/` — конфигурация веб-сервера nginx

---

