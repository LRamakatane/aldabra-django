"""beta.py
settings for beta environments

WARNING: This settings must not be used in production
to use this settings: set your the environment variable ENV=dev
"""

from config.settings.base import *
from config.settings.base import REST_FRAMEWORK, INSTALLED_APPS, MIDDLEWARE
from config.settings import getenv
from django.core.exceptions import ImproperlyConfigured
import environ
import os
from datetime import timedelta
import ssl

# from celery.schedules import crontab
# import sentry_sdk


TOKEN_EXPIRE_AT = 60

ALLOWED_HOSTS = ["*"]

# BETA APPS
# NOT ALL LIBRARIES
# HERE MIGHT MAKE IT TO
# PRODUCTION
BETA_APPS = [
    "knox",
]

INSTALLED_APPS.extend(BETA_APPS)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env.beta")
env.read_env(env_file)


def getvar(name: str):
    """tries to get the environmental vairable using\
         env or getenv.

        env is bound to this settings while getenv is global.
        getenv gets global, dynamic or user specific environmental\
            variables.
    """
    # first try getting the variable using env
    # if failed, then use getenv
    try:
        var = env(name)
    except ImproperlyConfigured:
        var = getenv(name)
    return var


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getvar("DBNAME"),
        "USER": getvar("DB_USER"),
        "PASSWORD": getvar("DB_PASSWORD"),
        "HOST": getvar("DB_HOST"),
        "PORT": getvar("DB_PORT"),
        "TEST": {
            "NAME": "auto_tests",
        },
        "CONN_MAX_AGE": 600,
    }
}


# MIDDLEWARE.insert(0, "config.middlewares.HTTPSRedirectMiddleware")
MIDDLEWARE.insert(1, "config.middlewares.CORSMiddleware")

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = [
    "https://booking-dashboard-staging.netlify.app",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://www.aajexpress.org",
]


# CORS_ALLOWED_ORIGIN_REGEXES = [
#    r"^https://\w+\.*\.com$",
# ]

CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "access-control-allow-origin",
]

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(minutes=TOKEN_EXPIRE_AT),
    "USER_SERIALIZER": "knox.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": 1,
    "AUTO_REFRESH": True,
    # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
}

# REST FRAMEWORK DEV SETTINGS

REST_FRAMEWORK.update(
    {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "services.authservice.backends.OAuth2ClientCredentialAuthentication",
            "knox.auth.TokenAuthentication",
        ),
        "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
        "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    }
)

# OAUTH2 BETA SETTINGS
# Set the access token expiration time to 1 hour (3600 seconds)
ACCESS_TOKEN_EXPIRE_SECONDS = 3600

OAUTH2_PROVIDER = {
    # parses OAuth2 data from application/json requests
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
    # this is the list of available scopes
    "SCOPES": {"read": "Read scope", "write": "Write scope"},
}

STATIC_URL = "/static/"
BASE_DIR = BASE_DIR.split("/")
BASE_DIR.pop()
BASE_DIR = "/".join(BASE_DIR)
STATIC_ROOT = BASE_DIR + "/static"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": getvar("REDIS_URI2"),
        # "OPTIONS": {"ssl_cert_reqs": None},
    }
}

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

heroku_redis_ssl_host = {
    "address": getvar("REDIS_URI"),  # The 'rediss' schema denotes a SSL connection.
    # "ssl_cert_reqs": None,
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                heroku_redis_ssl_host,
            ],
        },
    },
}


LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging configuration for errors
LOG_FILE_ERROR = os.path.join(LOG_DIR, "error.log")

# Logging configuration for access logs
LOG_FILE_ACCESS = os.path.join(LOG_DIR, "access.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_ERROR,
            "formatter": "verbose",
        },
        "access_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_ACCESS,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.server": {
            "handlers": ["access_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# # Celery settings
# CELERY_BROKER_URL = getvar("REDIS_URI")
# CELERY_RESULT_BACKEND = getvar("REDIS_URI")
# CELERY_TIMEZONE = "Africa/Lagos"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60


# CELERY_BEAT_SCHEDULE = {
#     "delete_schedule_quotes": {
#         "task": "services.orders.tasks.delete_scheduled_quotes",
#         "schedule": crontab(
#             hour=1,
#             minute=0,
#         ),
#     },
# }

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")

# # sentry settings
# sentry_sdk.init(
#     dsn="https://ae67933dee62123086003fe63dba779e@o4506469340348416.ingest.sentry.io/4506469347819520",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )

EMAIL_HOST_USER = getvar("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getvar("EMAIL_HOST_PASSWORD")
