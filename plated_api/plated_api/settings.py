"""
Django settings for plated_api project.
"""

from pathlib import Path

import environ  # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Take environment variables from .env file
env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))


SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "grades",
    "resources",
    "questions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "plated_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "plated_api.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env("DB_NAME", default=str(BASE_DIR / "db.sqlite3")),
        "USER": env("DB_USER", default=""),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default=""),
        "PORT": env("DB_PORT", default=""),
    }
}


# cache

CACHES = {
    "default": {
        "BACKEND": env(
            "CACHE_BACKEND",
            default="django.core.cache.backends.locmem.LocMemCache",
        ),
        "LOCATION": env("CACHE_LOCATION", default="unique-snowflake"),
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")

TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = env("USE_I18N", default=True)

USE_TZ = env("USE_TZ", default=True)


# Static files (CSS, JavaScript, Images)

STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = env("STATIC_ROOT", default=str(BASE_DIR / "static"))
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = env("MEDIA_ROOT", default=str(BASE_DIR / "media"))


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
