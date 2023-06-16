from pathlib import Path
import os

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='secretkeyissecrete')
DEBUG = env.bool('DEBUG', default=True)
ENVIRONMENT = env('ENVIRONMENT', default='development')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


LOCAL_INSTALLED_APPS = [
    'accounts',
    'budgets',
]
ADITIONAL_APPS = env.list('ADITIONAL_APPS', default=[])
INSTALLED_APPS = LOCAL_INSTALLED_APPS + ADITIONAL_APPS + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
]


ADITIONAL_MIDDLEWARE_START = env.list('ADITIONAL_MIDDLEWARE_START', default=[])
ADITIONAL_MIDDLEWARE_END = env.list('ADITIONAL_MIDDLEWARE_END', default=[])
MIDDLEWARE = ADITIONAL_MIDDLEWARE_START + [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] + ADITIONAL_MIDDLEWARE_END


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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


WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ("en-us", "English"),
    ("pt-BR", "Português"),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.UserProfile'

# ########## LOGGING ##########
LOGGING_LEVEL = env('LOGGING_LEVEL', default='INFO')
LOGGING_VERBOSE = env('LOGGING_VERBOSE', default='verbose')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} | {name}.{funcName}():{lineno:d}: {message}',
            'datefmt': '%d/%b/%Y %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': LOGGING_VERBOSE,
        },
    },
    'root': {
        'level': LOGGING_LEVEL,
        'handlers': ['console'],
        'propagate': True,
    },
    'loggers': {
        'fontTools': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': True,
        },
    }
}
