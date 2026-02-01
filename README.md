# shop-mini-app

**A mini-shop implemented with Django using templates, designed for the Telegram mini-app interface.**

Project features:

- Ability to open a chat with the seller, where the message text describing the interested product is automatically prefilled.
- Use of the `django-mptt` module to organize category hierarchy and optimize database queries.
- The `master` branch includes a ready-to-use `docker-compose.yml` that runs 3 services:
  - `web` — the Django application
  - `postgres` — PostgreSQL database server
  - `nginx` — web server

---

## Interface screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/main_page.jpg" alt="Main page" width="250"/>
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/main_page_sortings.jpg" alt="sortings" width="250"/>
  <img src="https://raw.githubusercontent.com/hurtki/shop-mini-app/assets/assets/inspect_page.jpg" alt="product page" width="250"/>
</p>

## [Deploy Instructions(link)](DEPLOY.md)

## Project structure

---

**Django Project Structure Overview:**

- **`Dockerfile`** — Docker configuration to build the app container.
- **`gunicorn.py`** — Gunicorn server configuration script.
- **`media/`** — User-uploaded media files, including product photos and previews.
- **`requirements.txt`** — Python dependencies list for the project.
- **`shop/`** — Main Django app folder containing:
  - `models.py`, `views.py`, `admin.py` — core app logic and admin interface.
  - `services.py`, `mixins.py`, `validators.py`, `utils.py` — helpers and business logic.
  - `migrations/` — database migration files.
  - `static/` and `templates/` — app-specific static files and HTML templates.
  - `templatetags/` — custom Django template tags.

- **`shop_tg_app/`** — Django project configuration directory with:
  - `settings.py` — main settings.
  - `urls.py` — URL routing.
  - `asgi.py`, `wsgi.py` — ASGI and WSGI entrypoints.

- **`static/`** — Collected static files for deployment, includes admin and third-party static assets.

---
