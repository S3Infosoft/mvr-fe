import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'atnvxcapm%14e+m-o6fk!#o_i4q8yaebpfiko+&2-1=ct!bk6-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.1.33.6', "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "users.apps.UsersConfig",

    # Packages
    "rest_framework",
    "import_export",
    "easyaudit",
    "debug_toolbar",

    # Apps
    "enquiry.apps.EnquiryConfig",
    "schedules.apps.SchedulesConfig",
]

MIDDLEWARE = [
    # django-debug-toolbar middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django-easy-audit middleware
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, "static"),
STATIC_ROOT = "/vol/web/static_root/"

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_URL = "login"
LOGOUT_URL = "logout"

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "login"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOG_DIR = "/vol/logs/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format": {
            "format": "%(levelname)s: %(filename)s: %(asctime)s: %(message)s",
        }
    },

    "handlers": {
        "auth_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR + "/auth.log",
            "formatter": "format",
        },
        "api_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR + "/api.log",
            "formatter": "format",
        }
    },

    "loggers": {
        "auth": {
            "handlers": ["auth_file"],
            "level": "INFO",
            "propagate": True,
        },
        "api": {
            "handlers": ["api_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = "/vol/web/media/"

# django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True

# django-easy-audit
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False
DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = ["users.CustomUser"]

# django-debug-toolbar
INTERNAL_IPS = ["localhost"]
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 75,
        "OPTIONS": {
            "MAX_ENTRIES": 1000
        }
    }
}
