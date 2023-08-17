import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'core/templates')


# Application definition

INSTALLED_APPS = [
    # Default Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    # 3rd Party
    # captchanotimeout is a custom app to override "captcha" to prevent 2 minute timeouts
    # See: https://github.com/praekelt/django-recaptcha/issues/183
    'captchanotimeout',
    'captcha',
    'embed_video',
    'debug_toolbar',
    'ckeditor',
    'rest_framework',
    'django_admin_listfilter_dropdown',
    # Custom
    'account',
    'general',
    'corpus',
    'help'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'settings_value': 'core.templatetags.settings_value',
            }
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Redirects for login and logout

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/account/login/'


# Custom user model

AUTH_USER_MODEL = 'account.User'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static/')
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# Media files (user uploaded content)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Clickjacking - allow content from this website
# https://docs.djangoproject.com/en/4.0/ref/clickjacking/

X_FRAME_OPTIONS = "SAMEORIGIN"


# Default primary key field type
# https://docs.djangoproject.com/en/latest/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CKEditor configuration options
# For full list of toolbar options see:
# https://ckeditor.com/latest/samples/old/toolbar/toolbar.html
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_CustomToolbarConfig': [
            {
                'name': 'tools',
                'items': [
                    'NumberedList', 'PasteText', 'Source',
                    '-',
                    'Outdent', 'Indent', 'BidiLtr', 'BidiRtl',
                    '-',
                    'Bold', 'Italic', 'Underline', 'Strike',
                    '-',
                    'Undo', 'Redo',
                    '-',
                    'Maximize',
                ]
            },
        ],
        'toolbar': 'CustomToolbarConfig',
        'enterMode': 2,
        'format_tags': 'p;h4',
        'tabSpaces': 4,
        'height': '27em',
        'width': '36.5em',
        'allowedContent': True
    }
}


# Import local_settings.py
try:
    from .local_settings import *  # NOQA
except ImportError:
    sys.exit('Unable to import local_settings.py (refer to local_settings.example.py for help)')

# Ensure required content from local_settings.py are supplied
if not SECRET_KEY:  # NOQA
    sys.exit('Missing SECRET_KEY in local_settings.py')


# Storages

# Default STORAGES from Django documentation
# See: https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Use ManifestStaticFilesStorage when not in debug mode
if not DEBUG:  # NOQA
    STORAGES['staticfiles'] = {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"}
