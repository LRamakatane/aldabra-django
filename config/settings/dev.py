"""dev.py
settings for dev environments

WARNING: This settings must not be used in production
to use this settings: set your the environment variable ENV=dev
"""
from config.settings.base import *
from config.settings.base import REST_FRAMEWORK, INSTALLED_APPS
from config.settings import getenv
from django.core.exceptions import ImproperlyConfigured
import environ
import os
from datetime import timedelta
# import ssl

TOKEN_EXPIRE_AT = 60

ALLOWED_HOSTS = ["*"]

# CSRF_TRUSTED_ORIGINS = ["https://booking-api-dev.aajexpress.org"]

# DEV APPS
# NOT ALL LIBRARIES
# HERE MIGHT MAKE IT TO
# STAGING OR PRODUCTION
DEV_APPS = ["knox", "drf_yasg", "drf_standardized_errors"]

INSTALLED_APPS.extend(DEV_APPS)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, "envs/env.dev")
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
        "CONN_MAX_AGE": 600,
    }
}

CORS_ORIGIN_ALLOW_ALL = True

REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(days=5),
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
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    }
)

# OAUTH2 DEV SETTINGS
OAUTH2_PROVIDER = {
    # parses OAuth2 data from application/json requests
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
    # this is the list of available scopes
    "SCOPES": {"read": "Read scope", "write": "Write scope"},
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Set STATIC_ROOT to the directory where you want to collect static files during deployment
STATIC_ROOT = "/var/www/booking-dev-staticfiles"

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": getvar("REDIS_URI"),
#         # "OPTIONS": {"ssl_cert_reqs": None},
#     }
# }

# ssl_context = ssl.SSLContext()
# ssl_context.check_hostname = False

# heroku_redis_ssl_host = {
#     "address": getvar("REDIS_URI2"),  # The 'rediss' schema denotes a SSL connection.
#     # "ssl_cert_reqs": None,
# }

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [
#                 heroku_redis_ssl_host,
#             ],
#         },
#     },
# }


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
# CELERY_BROKER_URL = getvar("REDIS_URI2")
# CELERY_RESULT_BACKEND = getvar("REDIS_URI2")
# # CELERY_BROKER_URL = "redis://localhost:6379"
# # CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_TIMEZONE = "Africa/Lagos"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"


# CELERY_BEAT_SCHEDULE = {
#     "delete_schedule_quotes": {
#         "task": "services.orders.tasks.delete_scheduled_quotes",
#         "schedule": crontab(
#             hour="0",
#             minute="0",
#         ),
#     },
#     "send_shipments": {
#         "task": "services.orders.tasks.send_shipments",
#         "schedule": crontab(hour="14", minute="45"),
#     },
# }


# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# EMAIL_HOST_USER = getvar("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = getvar("EMAIL_HOST_PASSWORD")

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"

TRUSTED_ORIGINS = ["*"]
