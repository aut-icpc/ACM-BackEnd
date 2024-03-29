"""
Django settings for icpcsite project.
Generated by 'django-admin startproject' using Django 2.2.3.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') ==  '1'

ALLOWED_HOSTS = [
    'localhost',
    os.getenv('RUNNING_HOST'),
    'api.icpc.aut.ac.ir'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'rest_framework',
    'corsheaders',
    'photologue',
    'sortedm2m',
    'django_rq',

    'contests',
    'mainsite',
    'usermanagement',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'icpcsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'icpcsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR+ '/'+ 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {

            # Local:
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DATABASE_NAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT')
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Django-Rq data
# https://github.com/rq/django-rq

REDIS_MAIL_URL = os.getenv('REDIS_MAIL_URL', 'redis://redis:6379/0')
REDIS_LIMIT_URL = os.getenv('REDIS_LIMIT_URL', 'redis://redis:6379/1')
MAILING_LIMIT = float(os.getenv('MAIL_LIMIT', 95))
MAIL_DELAY = int(os.getenv('MAIL_DELAY_SEC', 10))

RQ_QUEUES = {
    'emails': {
        'URL': REDIS_MAIL_URL,
        'DEFAULT_TIMEOUT': 500,
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

WWW_DIR = os.getenv('WWW_DIR')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WWW_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


## Should be uncommented in production!
# CORS_ORIGIN_WHITE_LIST = [
#     os.getenv('WHITELIST'),
# ]

MEDIA_ROOT = os.path.join(WWW_DIR, 'images')
MEDIA_URL = '/images/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'AUT-ICPC')
EMAIL_USE_TLS = True
EMAIL_PORT = int(os.getenv('EMAIL_PORT') or 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

## Should be commented in production!
CORS_ORIGIN_ALLOW_ALL = True

SITE_ID = 1

GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('GOOGLE_RECAPTCHA_SECRET_KEY')
