"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!km=w2#26v=qbqjw@6$6xut*3&3jlfu&r-r-kns=uo(r1ae)md'

# Create Google RECAPTCHA public and private keys: https://www.google.com/recaptcha/
RECAPTCHA_PUBLIC_KEY = 'xxxxx'
RECAPTCHA_PRIVATE_KEY = 'xxxxx'

DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'invisible-east.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'invisible-east_TEST.sqlite3'),
        },
    }
}

MAIN_CONTACT_EMAIL = 'mikeallaway@ahrsoftware.co.uk'

if DEBUG is True:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = '587'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'sender account email address'
    EMAIL_HOST_PASSWORD = 'sender account password'
    DEFAULT_FROM_EMAIL = 'from email address or Project Name (do not reply)'

ADMINS = [('Admin name', 'adminname@gmail.com')]
