"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ansufci#sg4%w)o22#q)#9qfy3s-2yf)gl!_$3elbj4ttn7!--'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['feh-resplendent.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Parties
    'rest_framework',
    'corsheaders',
    'django_filters',
    
    # Local
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

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
        'DIRS': [],
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

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

REALMS = {'0': 'Askr',
        '1':'Embla' ,
        '2':'Nifl', 
        '3':'Múspell',
        '4':'Hel',
        '5':'Ljósálfheimr',
        '6':'Dökkálfheimr',
        '7':'Niðavellir',
        '8':'Jötunheimr'}

GAME_TITLES = {
    "FEH":"Fire Emblem Heroes",
    "FE1":"Fire Emblem: Mystery of the Emblem",
    "FE3":"Fire Emblem: New Mystery of the Emblem",
    "FE2":"Fire Emblem Echoes: Shadows of Valentia",
    "FE4":"Fire Emblem: Genealogy of the Holy War",
    "FE5":"Fire Emblem: Thracia 776",
    "FE6":"Fire Emblem: The Binding Blade",
    "FE7":"Fire Emblem: The Blazing Blade",
    "FE8":"Fire Emblem: The Sacred Stones",
    "FE9":"Fire Emblem: Path of Radiance",
    "FE10":"Fire Emblem: Radiant Dawn",
    "FE11":"Fire Emblem Awakening",
    "FE12":"Fire Emblem Fates",
    "FE13":"Fire Emblem: Three Houses",
    "TMS":"Tokyo Mirage Sessions ＃FE Encore"
}

# --------------------  EDITS ------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

CORS_ALLOWED_ORIGINS = [
f"http://localhost:{os.environ.get('PORT', 3000)}",
f"http://127.0.0.1:{os.environ.get('PORT', 3000)}",
f"https://feh-resplendent.herokuapp.com:{os.environ.get('PORT', 3000)}"
]