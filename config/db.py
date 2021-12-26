import sys

from django.db import Error

from decouple import config


def get_correct_db_configuration(app_name):
    host = '/cloudsql/funeraria-edgar-angerosa:us-central1:funeraria-edgar-angerosa-db-instance'
    user = config('PRODUCTION_DB_USER')
    password = config('PRODUCTION_DB_PASSWORD')
    port = '5432'

    if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'createsuperuser' in sys.argv:
        host = 'localhost'
        port = '3306'

    if app_name == 'develop':
        host = 'localhost'
        user = config('DEVELOPMENT_DB_USER')
        password = config('DEVELOPMENT_DB_PASSWORD')
        name = 'skollars develop'
        port = '5432'
    elif app_name == 'testing':
        name = 'testing-db'
    elif app_name == 'applications.mortuary.apps.MortuaryConfig':
        name = 'funeraria-edgar-angerosa-db'
    elif app_name == 'applications.shooting_range.apps.ShootingRangeConfig':
        name = 'poligono-guillermo-echartea-db'
    elif app_name == 'applications.enchanted_house.apps.EnchantedHouseConfig':
        name = 'casa-encantada-veronica-db'
    else:
        raise Error("That app_name: {} does not have a db name associated.".format(app_name))

    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': host,
            'USER': user,
            'PASSWORD': password,
            'NAME': name,
            'PORT': port,
        }
    }
