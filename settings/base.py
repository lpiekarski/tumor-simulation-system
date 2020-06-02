import os.path
from os import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0#_#md((*!!yi!a$sto2k!w&!jla=wk9y(j#p5v0e=vnwnb$lz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'core',
    'homepage',
    'profiles',
    'simulations',
    'protocols',
    'apiv1',

    'django_extensions',
    'rest_framework',
    'guardian',
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

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                "core.context_processors.core_values",
                "core.context_processors.current_path",
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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

ADMIN_URL_BASE = environ.get('ADMIN_URL_BASE', r"^admin/")

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = STATIC_DIR
STATIC_URL = '/static/'

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

SITE_TITLE = "TSS"
SITE_TITLE_FULL = "Tumor Simulation System"

PROTOCOL_TIME_STEP = 6  # minutes

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

DEFAULT_CAROUSEL_IMAGE = '/static/images/default_carousel_background.jpg'

AVATAR_PROVIDER = 'https://www.tinygraphs.com/labs/isogrids/hexa/'

SSERVER_REFRESH_RATE = 30  # seconds
SIMULATION_EXECUTABLE = os.path.join(STATIC_DIR, 'bin/run_simulation')

SIMULATION_IMAGE_SETTINGS = {
    'SIMW_min': 0,
    'SIMW_max': 1,
    'SIMCHO_min': 0,
    'SIMCHO_max': 1e-12,
    'SIMOX_min': 0,
    'SIMOX_max': 1e-13,
    'SIMGI_min': 0,
    'SIMGI_max': 1e-16,
    'SIMtimeInRepair_min': 0,
    'SIMtimeInRepair_max': 1,
    'SIMirradiation_min': 0,
    'SIMirradiation_max': 1,
    'SIMcellState_min': 0,
    'SIMcellState_max': 5,
    'SIMcellCycle_min': 0,
    'SIMcellCycle_max': 5,
    'SIMproliferationTime_min': 0,
    'SIMproliferationTime_max': 30,
    'SIMcycleChanged_min': 0,
    'SIMcycleChanged_max': 5,
    'SIMG1time_min': 0,
    'SIMG1time_max': 10,
    'SIMStime_min': 0,
    'SIMStime_max': 20,
    'SIMG2time_min': 0,
    'SIMG2time_max': 5,
    'SIMMtime_min': 0,
    'SIMMtime_max': 5,
    'SIMDtime_min': 0,
    'SIMDtime_max': 0.5
}

try:
    from settings.local import *
except ImportError as e:
    print("No local configuration file provided")
    pass
