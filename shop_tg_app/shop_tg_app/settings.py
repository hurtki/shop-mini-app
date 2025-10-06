import os
from pathlib import Path
# библиотека для работы с переменными окружения
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")  # Никогда не хардкодь секретку

# SECURITY WARNING: don't run with debug turned on in production!
# Getting DJANGO_DEBUG variable from enviroment, it was set up in docker-compose accordingly to dev/nossl/ssl type of deployment
# For dev=True, for nossl = False, for ssl = True
DEBUG = os.environ.get("DJANGO_DEBUG", False) in ["true", "True"]


allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
assert allowed_hosts is not None, "DJANGO_ALLOWED_HOSTS is not set"
ALLOWED_HOSTS = allowed_hosts.split(",")

# static files paths
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# folder for storing media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Seller telegramm username 
# Redirecting to there when clicking BUY button on inspect page
TG_USERNAME = "VoidMgr"

# Allowed sorts ( for url, it won't create new buttons in UI) 
ALLOWED_SORTS = ["created_at", 'price', '-price', '-created_at']

# Limitations on the size of the search string used to search for products
MAX_SEARCH_CHARACTERS = 15
MIN_SEARCH_CHARACTERS = 3

# CSRF cookies with ssl settings 
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# limit how many posta will be shown on the first/main page  
# for no limit set: -1
MAX_POSTS_ON_MAIN_PAGE = -1

# quality of webp preview 50 to 100
# preview pictures are used on all pages except inspect page
# 50 - low quality, 100 - high quality 
WEBP_QUALITY = 75

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    # library for creating trees, for categories
    'mptt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CACHE SETTINGS FOR DOCKER REDIS SERVICE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1', # <---
    }
}



ROOT_URLCONF = 'shop_tg_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop_tg_app.wsgi.application'




BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
# static files storage setting
if DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
else:
    # here is a ManifestStaticFilesStorage to avoid caching old static files and create new versions
    # you can read more on django docs ( search for ManifestStaticFilesStorage)
    # https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/ 
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
        },
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
