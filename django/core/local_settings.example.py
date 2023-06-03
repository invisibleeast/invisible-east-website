"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create a SECRET_KEY.
# Online tools can help generate this for you, e.g. https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

# Create Google RECAPTCHA public and private keys: https://www.google.com/recaptcha/
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

# Set to True if in development, or False is in production
DEBUG = True/False

# Set to ['*'] if in development, or specific IP addresses and domains if in production
ALLOWED_HOSTS = ['*']/['invisible-east.org']

# Used by Django Debug Toolbar (comment out to disable DDT)
INTERNAL_IPS = ["127.0.0.1"]

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'invisible-east.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'invisible-east_TEST.sqlite3'),
        },
    }
}

# Provide a unique code that new users will need to input when creating a new account
ACCOUNT_CREATE_CODE = 'xxxxx'

# Provide the email address for the main contact for the project (e.g. the researcher/research team)
MAIN_CONTACT_EMAIL = '...@uni.ac.uk'

# Email
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

# Report system errors to the following people
ADMINS = [('Admin name', 'adminname@gmail.com')]
