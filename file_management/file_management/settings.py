"""
Django settings for file_management project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b9^5+)(%5&=c1$e5+(+5315e$8#f!2sw0&4ts=asipi6xy(5o-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'documents.apps.DocumentsConfig',
    'templateuri.apps.TemplateuriConfig',
    'log_module.apps.LogModuleConfig',
    'widget_tweaks',
    'datetimewidget',
    'django_nose',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'file_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.role_types.user_roles'
            ],
        },
    },
]


WSGI_APPLICATION = 'file_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

AUTH_PROFILE_MODULE = 'user.UserProfile'

LOGIN_URL = '/user/login/'

MEDIA_ROOT = 'file_management/files'
MEDIA_ROOT_URL = '/files'

PROJECT_DIR = os.path.dirname(__file__)

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'staticfiles'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'dbhandler': {
            'level': 'INFO',
            'class': 'file_management.log_handlers.SQLiteHandler',
        },
    },
    'filters': {
        'userAndDocumentFilter': {
            '()': 'file_management.log_filters.UserAndDocumentFilter',
        },
    },
    'loggers': {
        'documents': {
            'handlers': ['dbhandler'],
            'filters': ['userAndDocumentFilter'],
            'level': 'INFO',
            'propagate': True,
        },
        'users': {
            'handlers': ['dbhandler'],
            'filters': ['userAndDocumentFilter'],
            'level': 'INFO',
            'propagate': True,
        },
        'flows': {
            'handlers': ['dbhandler'],
            'filters': ['userAndDocumentFilter'],
            'level': 'INFO',
            'propagate': True,
        },
        'templates': {
            'handlers': ['dbhandler'],
            'filters': ['userAndDocumentFilter'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}