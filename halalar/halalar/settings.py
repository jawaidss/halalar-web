"""
Django settings for halalar project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'temp123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') != 'False'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_nose',
    'djrill',
    'storages',
    'captcha',
    'django_countries',
    'django_extensions',
    'push_notifications',
    'marketing',
    'legal',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'halalar.urls'

WSGI_APPLICATION = 'halalar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'halalar',
        'USER': 'halalar',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'temp123'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Kentucky/Louisville'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=marketing,legal,api',
    '--cover-html',
    '--nocapture',
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

SITE_ID = 1
SITE_DOMAIN = 'halalar.com'
SITE_NAME = 'Halalar'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'halalar.context_processors.site',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_FROM_EMAIL = '%s <salaam@%s>' % (SITE_NAME, SITE_DOMAIN)

SERVER_EMAIL = 'technical+django@%s' % SITE_DOMAIN

ADMINS = (
    (SITE_NAME, SERVER_EMAIL),
)

AWS_QUERYSTRING_AUTH = False

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    AWS_STORAGE_BUCKET_NAME = 'halalar-test'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    MAILCHIMP_LIST_ID = '07b7235072'
else:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
    EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

    DEFAULT_FILE_STORAGE = 'halalar.storages.MediaS3BotoStorage'
    STATICFILES_STORAGE = 'halalar.storages.StaticS3BotoStorage'

    MAILCHIMP_LIST_ID = '0bfa358826'

ALLOWED_HOSTS = [
    '.%s' % SITE_DOMAIN,
]

AWS_BACKUP_BUCKET_NAME = 'halalar-backup'

ASANA_EMAIL = 'x+18207867958361@mail.asana.com'

PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': os.environ['GCM_API_KEY'],
    'APNS_CERTIFICATE': os.environ['APNS_CERTIFICATE'],
}