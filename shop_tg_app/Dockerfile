# Используем минимальный образ Python
FROM python:3.12-slim

# Обновляем pip, устанавливаем зависимости ОС (если нужно)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём системного пользователя и группу для безопасности
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj

# Настройки Python: без .pyc и с немедленным выводом логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновляем pip
RUN pip install --upgrade pip


WORKDIR /app/www/shop_tg_app

# Копируем зависимости отдельно — это даёт кэш при пересборке
COPY ../requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Меняем пользователя на непривилегированного
USER userdj


CMD gunicorn -c gunicorn.py shop_tg_app.wsgi
