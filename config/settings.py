import os
import sys

from django.db import Error
from django.utils.translation import gettext_lazy as _

from config.db import get_correct_db_configuration
from decouple import config
from unipath import Path

# region ENVIRONMENT DEPENDANT CONFIGURATIONS: CHANGE!
DEBUG = True
LOCAL_APPS = ['applications.mortuary.apps.MortuaryConfig', 'applications.shooting_range.apps.ShootingRangeConfig',
              'applications.enchanted_house.apps.EnchantedHouseConfig']
ENVIRONMENT = 'development'  # Choices are: 'development' | 'testing' | 'production'
# endregion

# region Environment dependant configurations (depend on PRODUCTION: shouldn't be changed)
if ENVIRONMENT == 'development':
    DATABASES = get_correct_db_configuration(app_name='develop')
elif ENVIRONMENT == 'testing':
    ALLOWED_HOSTS = ['testing-275907.uc.r.appspot.com']
    DATABASES = get_correct_db_configuration(app_name='testing')
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 60
    SECURE_REDIRECT_EXEMPT = [r'.*mortuary\/generate_bills_for_monthly_clients\/$']
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
elif ENVIRONMENT == 'production':
    if len(LOCAL_APPS) > 1:
        raise Error('Be sure to install only one app at a time in production.')
    ALLOWED_HOSTS = ['funeraria-edgar-angerosa.uc.r.appspot.com', 'poligono-guillermo-echartea.uc.r.appspot.com',
                     'casa-encantada-veronica.uc.r.appspot.com']
    DATABASES = get_correct_db_configuration(app_name=LOCAL_APPS[0])
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 60
    SECURE_REDIRECT_EXEMPT = [r'.*mortuary\/generate_bills_for_monthly_clients\/$']
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
else:
    raise Error("Allowed environment choices are: 'development' | 'testing' | 'production'.")
# endregion

# region Environment agnostic configurations (shouldn't change often...)
# Standard Configs
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]
BASE_DIR = Path(__file__).parent.parent
SECRET_KEY = config('SECRET_KEY')
DJANGO_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
               'django.contrib.messages', 'django.contrib.staticfiles', ]
EXTERNAL_APPS = []
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.locale.LocaleMiddleware', 'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', ]
ROOT_URLCONF = 'config.urls'
sys.path.insert(0, os.path.join(BASE_DIR, 'applications'))
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                                 'django.template.context_processors.request',
                                                 'django.contrib.auth.context_processors.auth',
                                                 'django.contrib.messages.context_processors.messages', ], }, }, ]

# Internationalization
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES = [('en', _('English')), ('es', _('Spanish'))]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# endregion
