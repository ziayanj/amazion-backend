from .common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e+-)u(jx55$290)b1n+m1d70cg4be(!n*8dxxh5iw&r$8(tyz)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amazion',
        'USER': 'dev',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
