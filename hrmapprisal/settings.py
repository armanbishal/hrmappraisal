"""
Django settings for hrmapprisal project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import logging.config
import time
import pymysql
pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$g)8o+ksdor-q1f@3h4+knf%%wbe*ocg3txq4=n+u(x!$#f$o8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usermanagement',
    'configuration',
    'kpimanagement',
    'report',
    'billmanagement',
    'requisitionfrom'
]

AUTH_USER_MODEL = 'usermanagement.User'
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hrmapprisal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'hrmapprisal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appraisal',
        'USER': 'ipdc',
        'PASSWORD': 'Ipdc@321',
        'HOST': '192.168.7.117',
        'PORT': '',

        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'appraisal_test_hrm',
        # 'USER': 'root',
        # 'PASSWORD': 'sohel1234',
        # 'HOST': 'localhost',
        # 'PORT': '',
    }}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

HRMLOGIN = "http://182.163.112.216/SE/MasterPanel/Account/LoginByQMS"
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def log_setting():
    global log
    log = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': "%(asctime)s.%(msecs)03d  %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': '%d/%m/%Y %H:%M:%S',

                # 'datefmt': "%d/%b/%Y %H:%M:%S %p"
            },
            'simple': {
                'format': "{levelname} {message} ",
                'datefmt': '%d/%m/%Y %H:%M:%S',
                'style': '{',
            },
            'verbose': {
                'format': '{asctime} {msecs} {levelname} {message} ',
                'datefmt': '%d/%m/%Y %H:%M:%S',
                'style': '{',
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'logfile': {
                'level': 'INFO',
                # 'class': 'logging.handlers.RotatingFileHandler',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'midnight',
                # 'interval': 3,
                # 'filename': 'log_stack/mylog.log',
                # 'filename': 'log_stack/' + str(time.strftime("%b %d %Y ", time.localtime())) + '.log',
                'filename': 'log_stack/' + str(time.strftime("%d-%m-%Y", time.localtime())) + '.log',
                # 'maxBytes': 1000000,
                'backupCount': 50,
                # 'formatter': 'standard',
                'formatter': 'standard',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'email_backend': 'django.core.mail.backends.filebased.EmailBackend',
            },
        },
        'loggers': {
            'usermanagement': {
                'handlers': ['console', 'logfile', ],  # 'elasticsearch'
                'level': 'INFO',
            },
            'configuration': {
                'handlers': ['console', 'logfile', ],
                'level': 'INFO',
            },
            'transaction': {
                'handlers': ['console', 'logfile', ],  # 'elasticsearch'
                'level': 'DEBUG',
                # 'propagate': True,

            },
            'report': {
                'handlers': ['console', 'logfile', ],  # 'elasticsearch'
                'level': 'DEBUG',
                # 'propagate': True,

            },
            'api': {
                'handlers': ['console', 'logfile', ],  # 'elasticsearch'
                'level': 'DEBUG',
            },
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            },
        }
    }
    # print("yes")
    return log