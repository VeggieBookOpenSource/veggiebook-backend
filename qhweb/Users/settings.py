# coding=utf-8
#
# Copyright © 2020 Quick Help For Meals, LLC. All rights reserved.
#
# This file is part of VeggieBook.
#
# VeggieBook is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the license only.
#
# VeggieBook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or fitness for a particular purpose. See the
# GNU General Public License for more details.
#

# Django settings for Users project.

import os
from ConfigParser import RawConfigParser, NoOptionError
import djcelery
import uuid
uuid._uuid_generate_random = None

djcelery.setup_loader()

os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
print DIRNAME

config = RawConfigParser()
config.read('/etc/qhmobile/settings.ini')


def configDirsToTuple(dirStr):
    l = dirStr.split(',')
    return tuple([p if os.path.isabs(p) else os.path.join(DIRNAME, p) for p in l])


DEBUG = config.getboolean('debug', 'DEBUG')
TEMPLATE_DEBUG = config.getboolean('debug', 'TEMPLATE_DEBUG')

ADMINS = (
    ('admin', 'ddipasquo@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': config.get('database', 'DATABASE_NAME'), # Or path to database file if using sqlite3.
        'USER': config.get('database', 'DATABASE_USER'), # Not used with sqlite3.
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'), # Not used with sqlite3.
        'HOST': config.get('database', 'DATABASE_HOST'),
        #'localhost',#'qhmobile.ci9ey74meneu.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': config.get('database', 'DATABASE_PORT'), # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIRNAME, config.get('storage', 'STATIC_ROOT'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
try:
    STATICFILES_DIRS = config.get('storage', 'STATICFILES_DIRS')
except NoOptionError:
    STATICFILES_DIRS = ''

STATICFILES_DIRS = configDirsToTuple(STATICFILES_DIRS)

# (
#    # Put strings here, like "/home/html/static" or "C:/www/django/static".
#    # Always use forward slashes, even on Windows.
#    # Don't forget to use absolute paths, not relative paths.
#    #os.path.join(DIRNAME, 'qhmobileStatic/'),
#    '/Library/Python/2.7/site-packages/django_extensions/static',
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('django', 'SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',)

MIDDLEWARE_CLASSES = (
#    'johnny.middleware.LocalStoreClearMiddleware',
#    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'qhmobile.middleware.AcceptMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'qhmobile.auth.GoogleTokenBackend',
    'qhmobile.auth.DeviceIdBackend'
)

LOGIN_REDIRECT_URL = '/static/qhmobile/recipes_loading.html'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

ROOT_URLCONF = 'Users.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Users.wsgi.application'

# TEMPLATE_DIRS = ('/Users/danieldipasquo/qhmobile/Users/templates',)

TEMPLATE_DIRS = configDirsToTuple(config.get('storage', 'TEMPLATE_DIRS'))
#TEMPLATE_DIRS = (os.path.join(DIRNAME,'Users/templates'),os.path.join(DIRNAME,'qhmobile/templates'),os.path.join(DIRNAME,'templates'),'/opt/django_extensions/templates')

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    'imagekit',
    'djcelery',
    'gunicorn',
    'qhmobile',
    'storages',
    'easy_maps',
]

INSTALLED_APPS = tuple(INSTALLED_APPS)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#AWS S3 Storage Settings
DEFAULT_FILE_STORAGE = config.get('aws', 'DEFAULT_FILE_STORAGE')
AWS_ACCESS_KEY_ID = config.get('aws', 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('aws', 'AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config.get('aws', 'AWS_STORAGE_BUCKET_NAME')

AWS_QUERYSTRING_AUTH = False
STATICFILES_STORAGE = config.get('storage', 'STATICFILES_STORAGE')

APPEND_SLASH = True

CACHES = {
    'default': {
        'BACKEND': config.get('cache', 'BACKEND'),
        'LOCATION': config.get('cache', 'LOCATION'),
    }
}


#JOHNNY_MIDDLEWARE_KEY_PREFIX = config.get('cache', 'CACHE_PREFIX')

#Celery Settings for asynchronous tasks
CELERY_TASK_SERIALIZER = 'json'

WKHTMLTOPDF_CMD = os.path.join(DIRNAME, 'wh2p')

SITE_PROTOCOL = config.get('site', 'SITE_PROTOCOL')

EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_PORT = config.getint('email', 'EMAIL_PORT')
EMAIL_USE_TLS = config.getboolean('email', 'EMAIL_USE_TLS')
EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')

MOBI_DETECT_TABLET = True


SOUTH_MIGRATION_MODULES = {
        'djcelery': 'djcelery.south_migrations',
    }

