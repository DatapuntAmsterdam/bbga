"""
Django settings for bbga project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from bbga.settings_databases import (LocationKey, get_database_key,
                                     get_docker_host)

OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

DIVA_DIR = '/app/data'

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

DEBUG = SECRET_KEY == 'default-secret'

NO_INTEGRATION_TESTS = True

ALLOWED_HOSTS = ['*']

DATAPUNT_API_URL = os.getenv(
    # note the ending /
    'DATAPUNT_API_URL', 'https://api.data.amsterdam.nl/')

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.postgres',
    'django_extensions',
    'datapunt_api',
    'bbga',
    'bbga_data',
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'health',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'bbga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbga.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'bbga'),
        'USER': os.getenv('DB_USER', 'bbga'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'bbga'),
        'USER': os.getenv('DB_USER', 'bbga'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5406'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'bbga'),
        'USER': os.getenv('DB_USER', 'bbga'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))


INTERNAL_IPS = ['127.0.0.1']

HEALTH_MODEL = 'bbga_data.Cijfers'

REST_FRAMEWORK = dict(
    PAGE_SIZE=25,
    MAX_PAGINATE_BY=8000,

    UNAUTHENTICATED_USER=None,
    UNAUTHENTICATED_TOKEN=None,

    DEFAULT_PAGINATION_CLASS='drf_hal_json.pagination.HalPageNumberPagination',
    DEFAULT_PARSER_CLASSES=('drf_hal_json.parsers.JsonHalParser',),
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'datapunt_api.renderers.PaginatedCSVRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    DEFAULT_FILTER_BACKENDS=(
        'django_filters.rest_framework.DjangoFilterBackend',),
    COERCE_DECIMAL_TO_STRING=False,
)

# SWAGGER

swag_path = 'acc.api.data.amsterdam.nl/bbga/docs'

if DEBUG:
    swag_path = '127.0.0.1:8000/bbga/docs'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',

    'enabled_methods': [
        'get',
    ],

    'api_key': '',
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,

    'is_authenticated': False,
    'is_superuser': False,

    'permission_denied_handler': None,
    'resource_access_handler': None,

    'protocol': 'https' if not DEBUG else '',
    'base_path': swag_path,

    'info': {
        'contact': 'atlas.basisinformatie@amsterdam.nl',
        'description': 'This is the BBGA API server.',
        'license': 'license Not known yet.',
        'licenseUrl': '://www.amsterdam.nl/stelselpedia/',
        'termsOfServiceUrl': 'https://data.amsterdam.nl/terms/',
        'title': 'BBGA',
    },

    'doc_expansion': 'list',
}

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', '127.0.0.1')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_GELF_UDP_PORT', 12201))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },

        'graypy': {
            'level': 'ERROR',
            'class': 'graypy.GELFHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT,
        },
    },

    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'graypy'],
    },

    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },

        # Debug all batch jobs
        'doc': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'index': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },

        'search': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'elasticsearch': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'urllib3': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        'factory.containers': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        'factory.generate': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        'requests.packages.urllib3.connectionpool': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Log all unhandled exceptions
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

    },
}
