# debug.py
from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

# WSGI application
WSGI_APPLICATION = 'config.wsgi.debug.application'

# Static URLs
# MEDIA폴더
#   octocolumn_project/.media/
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

# Static Root폴더
#   octocolumn_project/.static_root/


# Static폴더
#    octocolumn_project/instagram/static/
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_DIRS = [
    STATIC_DIR,
]

# Debug Mode so True
DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'corsheaders',

    # storages
    'storages',

    # rest_framework
    'rest_framework',
    'rest_framework.authtoken',

    'member',
    'column',

]

SITE_ID = 1
# Database
DATABASES = {
    'default': {
        'ENGINE': config_secret_debug['django']['databases']['engine'],
        'NAME': config_secret_debug['django']['databases']['name'],
        'USER': config_secret_debug['django']['databases']['user'],
        'PASSWORD': config_secret_debug['django']['databases']['password'],
        'HOST': config_secret_debug['django']['databases']['host'],
        'PORT': config_secret_debug['django']['databases']['port']
    }
}

# Storage settings
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
# STATICFILES_STORAGE = 'config.storages.StaticStorage'

FACEBOOK_APP_ID = config_secret_debug['accounts']['facebook']['app_id']
FACEBOOK_APP_SECRET_CODE = config_secret_debug['accounts']['facebook']['secret_code']


# Celery
# CELERY_BROKER_URL = 'redis://{}:{}'.format(
#     config_secret_debug['django']['celery']['broker_url'],
#     config_secret_debug['django']['celery']['broker_port']
# )
# CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(
#     config_secret_debug['django']['celery']['broker_url'],
#     config_secret_debug['django']['celery']['broker_port']
# )
# print(CELERY_BROKER_URL)
print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)


CORS_ORIGIN_ALLOW_ALL = True

