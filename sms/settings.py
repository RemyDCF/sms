"""
Django settings for sms project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get("DEBUG", str(True)))

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "sms.remydcf.dev"]
INTERNAL_IPS = ("127.0.0.1", "localhost")

# Application definition

INSTALLED_APPS = [
    "main.apps.MainConfig",
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "rest_framework",
    "maintenance_mode",
    "webpush",
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

ROOT_URLCONF = "sms.urls"
CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "maintenance_mode.context_processors.maintenance_mode",
            ]
        },
    }
]

WSGI_APPLICATION = "sms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if os.environ.get("POSTGRESQL_HOST", "") != "":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRESQL_NAME", ""),
            "USER": os.environ.get("POSTGRESQL_USER", ""),
            "PASSWORD": os.environ.get("POSTGRESQL_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRESQL_HOST", ""),
            "PORT": os.environ.get("POSTGRESQL_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "database.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BM7nNo7OFK5C-U3PRp45UuU-a4A7cfBBb4SFy6WjKOm4usgchbmnUMSuYh4vRrZ1BHX9UXcMgx19Efsn7G9AGbc",
    "VAPID_PRIVATE_KEY": "oVDpQ5HYi2OPyPjsSrTGhRNpnNneksS17BybZXvtAGw",
    "VAPID_ADMIN_EMAIL": "sms@remydcf.dev",
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MAINTENANCE_MODE_STATE_FILE_PATH = "maintenance_mode_state.txt"
TWILIO_ACCOUNT_SIDS = os.environ.get("TWILIO_ACCOUNT_SIDS", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")
REDIRECT_PHONE_NUMBER = os.environ.get("REDIRECT_PHONE_NUMBER", "")

GITHUB_WEBHOOK_KEY = os.environ.get("GITHUB_WEBHOOK_KEY", "")
