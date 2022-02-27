import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'app'),
        'USER': os.getenv('DB_USER', 'appuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'appuserpass'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 3306),
        'OPTIONS': {
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO'
        },
    }
}
