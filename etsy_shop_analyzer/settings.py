"""
Django settings for etsy_shop_analyzer project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import environ
import logging
import os
from pathlib import Path

from django.utils.log import DEFAULT_LOGGING

env = environ.Env(
    DEBUG=(bool, False),
    CLIENT_CONNECT_TIMEOUT=(float, 10.0),
    CLIENT_READ_TIMEOUT=(float, 60.0),

)


def optenv(var):
    return env(var, default=None)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']  # warnign! don't use * in production


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_admin_conf_vars'
]

OUR_APPS = [
    'apps.shop_analyzer',
]
INSTALLED_APPS += OUR_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'etsy_shop_analyzer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'etsy_shop_analyzer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),

    # read os.environ['SQLITE_URL']
    'extra': env.db_url(
        'SQLITE_URL',
        default='sqlite:////tmp/my-tmp-sqlite.db'
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env("STATIC_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGLEVEL = env('LOGLEVEL')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': [
                'console',
            ],
        },
        'huey': {
            'level': 'INFO',
            'handlers': [
                'console',
            ],
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}
# add env configurable logging to our apps only to prevent flooding the logs with django debug stuff
for app in OUR_APPS:
    LOGGING['loggers'][app] = {
        'level': LOGLEVEL,
        'handlers': [
            'console',
        ],
        'propagate': False,
    }
logging.config.dictConfig(LOGGING)

CLIENT_CONNECT_TIMEOUT = env('CLIENT_CONNECT_TIMEOUT')
CLIENT_READ_TIMEOUT = env('CLIENT_READ_TIMEOUT')

# Etsy data
ETSY_KEYSTRING = env('ETSY_KEYSTRING')
ETSY_SHARED_SECRET = env('ETSY_SHARED_SECRET')

# This variable can be getted using an etsy endpoint. Due to time we use it as a normal variable
# check the endpoint https://developers.etsy.com/documentation/reference/#operation/ping
ETSY_APP_ID = env('ETSY_APP_ID')

ETSY_SHOP_IDS = [
    17814318,  # HauntedStories
    14386188,  # Boorooroom
    9835674,  # CirquellCuriosities
    5125128,  # simbiosisbyjulia
    10956897,  # SuuperPaper
    21676911,  # BlendedExtreme
    7559854,  # SKYWORLDPROJECT
    12448432,  # moticas
    19746707,  # CursedByDesign
    15224627,  # DISEDINA
]
VARS_MODULE_PATH = 'etsy_shop_analyzer.global_vars'
