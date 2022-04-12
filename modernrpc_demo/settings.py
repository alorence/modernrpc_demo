"""
Django settings for modernrpc_demo project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import environ

# Configure the project's root
root = environ.Path(__file__, '../..')

# Configure some default for environment
env = environ.Env(DEBUG=(bool, False),)
# Try to load
environ.Env.read_env(root('.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='dummy_local_secret_key_xyz')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    'modernrpc.herokuapp.com',
    'localhost', '127.0.0.1', '[::1]',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'modernrpc',
    'analytical',

    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Immediately after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'modernrpc_demo.urls'

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

WSGI_APPLICATION = 'modernrpc_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', 'sqlite:///db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

ENABLE_DEBUG_LOGS = env.bool("ENABLE_DEBUG_LOGS", default=False)
if ENABLE_DEBUG_LOGS:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            # your other loggers configuration
            'modernrpc': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = root('static')

# Whitenoise static file compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Django-modern-rpc
MODERNRPC_METHODS_MODULES = [
    'main.rpc.math',
    'main.rpc.meta',
    'main.rpc.errors',
]

# Force HTTPS on production:
SECURE_SSL_REDIRECT = False  # not DEBUG

# Django-analytical
GOOGLE_ANALYTICS_JS_PROPERTY_ID=env.str('GOOGLE_ANALYTICS_PROPERTY_ID', default="")
GOOGLE_ANALYTICS_SITE_SPEED = True
GOOGLE_ANALYTICS_ANONYMIZE_IP = True
