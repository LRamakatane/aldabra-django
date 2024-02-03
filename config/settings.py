"""
Django settings for config project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from django.utils.timezone import timedelta
import ssl
from configurations import Configuration, values
from decouple import config as env

import environ

BASE_DIR = Path(__file__).resolve().parent.parent


class Common(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.

    # SECURITY WARNING: keep the secret key used in production secret!

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = ["*"]

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "django_extensions",
        "debug_toolbar",
        "core",
        "rest_framework",
        "drf_yasg",
        "coreapi",
        "corsheaders",
        "storages",
        "oauth2_provider",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "config.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "config.wsgi.application"

    APPEND_SLASH = True

    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/
    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "Africa/Lagos"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    AUTH_USER_MODEL = "core.User"

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    }

    # Cors headers
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
        }
    }

    AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

    LOGIN_URL = "/admin/login/"
    SITE_NAME = ""
    DOMAIN = ""

    # DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    # AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    # AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    # AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")

    # # set up for using MailGun SMTP backend
    # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    # EMAIL_HOST = "smtp.mailgun.org"
    # EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    # EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    # EMAIL_PORT = 465
    # EMAIL_USE_SSL = True
    # EMAIL_USE_TLS = False
    # DEFAULT_FROM_EMAIL = ""

    # Configure the logging settings
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # Ensure the logs directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Logging configuration for errors
    LOG_FILE_ERROR = os.path.join(LOG_DIR, "error.log")
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "error_file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOG_FILE_ERROR,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["error_file"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

    # Logging configuration for server prints
    LOG_FILE_SERVER = os.path.join(LOG_DIR, "server.log")
    LOGGING["handlers"]["server_file"] = {
        "level": "INFO",
        "class": "logging.FileHandler",
        "filename": LOG_FILE_SERVER,
        "formatter": "verbose",
    }
    LOGGING["loggers"]["django.server"] = {
        "handlers": ["server_file"],
        "level": "INFO",
        "propagate": False,
    }

    # Logging formatter
    LOGGING["formatters"] = {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }


class Local(Common):
    """
    The local developer settings for his computer and the default configuration.
    """

    env = environ.Env()

    env_file = os.path.join(BASE_DIR, "config/envs/.env.dev")

    env.read_env(env_file=env_file)

    SECRET_KEY = env("DJANGO_SECRET_KEY")

    MIDDLEWARE = Common.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    database_url = env("DATABASE_URL")

    DATABASES = values.DatabaseURLValue(database_url)

    DATABASES.default["CONN_MAX_AGE"] = 600

    INTERNAL_IPS = ["127.0.0.1"]

    MIDDLEWARE = Common.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    CORS_ORIGIN_ALLOW_ALL = True

    REST_KNOX = {
        "SECURE_HASH_ALGORITHM": "cryptography.hazmat.primitives.hashes.SHA512",
        "AUTH_TOKEN_CHARACTER_LENGTH": 64,
        "TOKEN_TTL": timedelta(hours=1),
        "USER_SERIALIZER": "knox.serializers.UserSerializer",
        "TOKEN_LIMIT_PER_USER": 1,
        "AUTO_REFRESH": True,
        # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
    }

    # REST FRAMEWORK DEV SETTINGS
    Common.REST_FRAMEWORK.update(
        {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "config.backends.OAuth2ClientCredentialAuthentication",
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

    # Celery settings
    # CELERY_BROKER_URL = env("REDIS_URI")
    # CELERY_RESULT_BACKEND = env("REDIS_URI")
    # CELERY_TIMEZONE = "Africa/Lagos"
    # CELERY_TASK_TRACK_STARTED = True
    # CELERY_TASK_TIME_LIMIT = 30 * 60
    # CELERY_ACCEPT_CONTENT = ["json"]
    # CELERY_TASK_SERIALIZER = "json"
    # CELERY_RESULT_SERIALIZER = "json"

    # print(CELERY_BROKER_URL)

    # CELERY_BEAT_SCHEDULE = {
    #     "delete_schedule_quotes": {
    #         "task": "services.orders.tasks.delete_scheduled_quotes",
    #         "schedule": crontab(
    #             hour=1,
    #             minute=0,
    #         ),
    #     },
    # }


class Development(Local):
    """
    The in-development settings and the default configuration.
    """

    env = environ.Env()

    env_file = os.path.join(BASE_DIR, "config/envs/.env.dev")

    env.read_env(env_file=env_file)

    TOKEN_EXPIRE_AT = 60

    CSRF_TRUSTED_ORIGINS = []

    # DEV APPS
    # NOT ALL LIBRARIES HERE MIGHT MAKE IT TO STAGING OR PRODUCTION
    DEV_APPS = ["knox", "drf_standardized_errors"]
    Common.INSTALLED_APPS.extend(DEV_APPS)

    CORS_ORIGIN_ALLOW_ALL = True

    # CACHES = {
    #     "default": {
    #         "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #         "LOCATION": env("REDIS_URI2"),
    #         # "OPTIONS": {"ssl_cert_reqs": None},
    #     }
    # }

    # ssl_context = ssl.SSLContext()
    # ssl_context.check_hostname = False

    # heroku_redis_ssl_host = {
    #     "address": env("REDIS_URI"),  # The 'rediss' schema denotes a SSL connection.
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


class Staging(Common):
    """
    The in-staging settings.
    """

    env = environ.Env()

    env_file = os.path.join(BASE_DIR, "config/envs/.env.staging")

    env.read_env(env_file=env_file)

    DEBUG = False

    SECRET_KEY = env("DJANGO_SECRET_KEY")

    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(("HTTP_X_FORWARDED_PROTO", "https"))

    CSRF_TRUSTED_ORIGINS = env("TRUSTED_ORIGINS").split(",")

    TOKEN_EXPIRE_AT = 60

    # BETA APPS
    # NOT ALL LIBRARIES HERE MIGHT MAKE IT TO PRODUCTION
    BETA_APPS = []

    Common.INSTALLED_APPS.extend(BETA_APPS)

    DATABASES = values.DatabaseURLValue(env("DATABASE_URL"))

    DATABASES = values.DatabaseURLValue(env("DATABASE_URL"))

    DATABASES.default["CONN_MAX_AGE"] = 600

    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        # 'localhost:3000',
        "http://127.0.0.1:3000",
        # '127.0.0.1:3000',
        "https://dashboard.aajexpress.org",
    ]

    # CORS_ALLOWED_ORIGIN_REGEXES = [
    #    r"^https://\w+\.*\.com$",
    # ]

    CORS_URLS_REGEX = r"^/api/.*$"

    CORS_ALLOW_ALL_ORIGINS = False

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
        "TOKEN_TTL": timedelta(hours=1),
        "USER_SERIALIZER": "knox.serializers.UserSerializer",
        "TOKEN_LIMIT_PER_USER": 1,
        "AUTO_REFRESH": True,
        # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
    }

    Common.REST_FRAMEWORK.update(
        {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "config.backends.OAuth2ClientCredentialAuthentication",
                "knox.auth.TokenAuthentication",
            ),
            "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
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

    # CACHES = {
    #     "default": {
    #         "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #         "LOCATION": env("REDIS_URI2"),
    #         "OPTIONS": {"ssl_cert_reqs": None},
    #     }
    # }

    # ssl_context = ssl.SSLContext()
    # ssl_context.check_hostname = False

    # heroku_redis_ssl_host = {
    #     "address": env("REDIS_URI"),  # The 'rediss' schema denotes a SSL connection.
    #     "ssl_cert_reqs": None,
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


class Production(Staging):
    """
    The in-production settings.
    """

    env = environ.Env()

    env.read_env(env_file="config/envs/.env.prod")
    DEBUG = False

    SECRET_KEY = env("DJANGO_SECRET_KEY")

    Common.MIDDLEWARE.insert(0, "config.middlewares.HTTPSRedirectMiddleware")
    Common.MIDDLEWARE.insert(1, "config.middlewares.CORSMiddleware")

    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        # 'localhost:3000',
        "http://127.0.0.1:3000",
        # '127.0.0.1:3000',
        "https://dashboard.aajexpress.org",
    ]

    # CORS_ALLOWED_ORIGIN_REGEXES = [
    #    r"^https://\w+\.*\.com$",
    # ]

    CORS_URLS_REGEX = r"^/api/.*$"

    CORS_ALLOW_ALL_ORIGINS = False

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
        "TOKEN_TTL": timedelta(hours=30),
        "USER_SERIALIZER": "knox.serializers.UserSerializer",
        "TOKEN_LIMIT_PER_USER": 1,
        "AUTO_REFRESH": True,
    }

    Common.REST_FRAMEWORK.update(
        {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "config.backends.OAuth2ClientCredentialAuthentication",
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

    # CACHING = {
    #     "default": {
    #         "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #         "LOCATION": env("REDIS_URI2"),
    #         "OPTIONS": {"ssl_cert_reqs": None},
    #     }
    # }

    # ssl_context = ssl.SSLContext()
    # ssl_context.check_hostname = False

    # heroku_redis_ssl_host = {
    #     "address": env("REDIS_URI"),  # The 'rediss' schema denotes a SSL connection.
    #     "ssl_cert_reqs": None,
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
