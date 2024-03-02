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
from datetime import timedelta
import os
# import ssl

TOKEN_EXPIRE_AT = 60

ALLOWED_HOSTS = ["*"]
# ["localhost" "ws", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = []

# DEV APPS
# NOT ALL LIBRARIES
# HERE MIGHT MAKE IT TO
# STAGING OR PRODUCTION
DEV_APPS = ["knox", "drf_yasg", "drf_standardized_errors"]
INSTALLED_APPS.extend(DEV_APPS)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, "envs/.env.local")
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


SECRET_KEY = env("DJANGO_SECRET_KEY")
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
        "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
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
BASE_DIR = BASE_DIR.split("/")
BASE_DIR.pop()
BASE_DIR = "/".join(BASE_DIR)
STATIC_ROOT = BASE_DIR + "/static"

# CACHING = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake",
#     }
# }

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": getvar("REDIS_URI2"),
#         "OPTIONS": {"ssl_cert_reqs": None},
#     }
# }

# CHANNEL_LAYER_SSL=True
# CHANNEL_LAYER_PROTO='redis'+'s'*CHANNEL_LAYER_SSL

# ssl_context = ssl.SSLContext()
# ssl_context.check_hostname = False

# heroku_redis_ssl_host = {
#     "address": getvar("REDIS_URI"),  # The 'rediss' schema denotes a SSL connection.
#     "ssl_cert_reqs": None,
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://localhost:6379",
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
