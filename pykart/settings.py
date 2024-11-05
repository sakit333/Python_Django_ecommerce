"""
Django settings for pykart project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4$p)=_$&cil8h($1p3@5tqj0rhcqa$(s7fsi!1n$2$@sw^7q-f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    "crispy_bootstrap4",
    'django_countries'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pykart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'pykart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DBNAME'),
        'USER' : os.environ.get('DBUSER'),
        'PASSWORD' :os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT' :os.environ.get('PORT'),
    }
}

# Attempt to create the database if it doesn't exist
db_name = DATABASES['default']['NAME']
db_user = DATABASES['default']['USER']
db_password = DATABASES['default']['PASSWORD']
db_host = DATABASES['default']['HOST']
db_port = int(DATABASES['default']['PORT'])

try:
    db_connection = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        port=db_port
    )
    db_connection.autocommit(True)
    cursor = db_connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' is ready.")
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    cursor.close()
    db_connection.close()


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR/'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

LOGIN_URL = '/signin/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

STRIPE_TEST_PUBLIC_KEY = 'pk_test_51Q850N2MG9Uo6huKvURRS8s9GkMsw1ZHMNzSDBjRxuFxVIhRyXo19RGBXT2YtuUhY5AtR1L5RhRb2gMQ2S2DnKt100Wsym1VhO'
STRIPE_TEST_SECRET_KEY = 'sk_test_51Q850N2MG9Uo6huKP6Eo6Nq1ctyXc9OfqhYoXlv45sAntjEwdQwL2SU40rcFw7ziyOxpGDvtR0dhuzuqDexfVyll00gTfpnNR7'