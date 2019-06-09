"""
Base settings to build other settings files upon.
"""
import os

from moistmaster.config import config


def sqlite_conn_path():
    return "{pth}/robosquirt.db".format(pth=config["sqlite_db_path"])


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(BASE_DIR, *x)
app = lambda *x: os.path.join(BASE_DIR, 'moistmaster', *x)


# GENERAL
# ------------------------------------------------------------------------------

DEBUG = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# APP
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'moistmaster.urls'
WSGI_APPLICATION = 'moistmaster.wsgi.application'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            'Q7Nnmm0lBJ7F6JLTPk6vpHJ2eciARLPSNqFGXBpHe7uk8dDoFowcoF9wZwOJJqPY')

# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'compressor',
    'crispy_forms',
    'localflavor',
]

PROJECT_APPS = [
    'analytics',
    'geo'
]

LOCAL_APPS = [
    'debug_toolbar',
]

INSTALLED_APPS += PROJECT_APPS

if DEBUG:
    INSTALLED_APPS += LOCAL_APPS


# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite_conn_path(),
    }
}


# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    app("static"),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [app("templates")],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(name)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
        },
        'moistmaster': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}


# ACCESS
# ------------------------------------------------------------------------------
LOGIN_URL = "login"
DEFAULT_USERNAME = "admin"


# ACCESS
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = [
    "*",
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# CRISPY FORMS
# ------------------------------------------------------------------------------
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application Settings
# ------------------------------------------------------------------------------
MAPBOX_TOKEN = config["mapbox_token"]
USGS_GNIS_DATA = os.path.join(BASE_DIR, "bundled_data", "USGS-GNIS-data-2019-20190501.txt")