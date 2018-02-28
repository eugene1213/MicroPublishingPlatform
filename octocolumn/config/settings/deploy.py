# deploy.py
from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'

STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')


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

    'django_s3_storage',

    'rest_framework',
    'rest_framework.authtoken',

    'member',
    'column',

]

# AWS settings
AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret_deploy['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = config_secret_deploy['aws']['s3_region_name']
AWS_QUERYSTRING_AUTH = False

S3_USE_SIGV4 = True

AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_S3_REGION_NAME
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Static Setting
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Media Setting
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


# 배포모드니까 DEBUG는 False
DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# Database
DATABASES = {
    'default': {
        'ENGINE': config_secret_deploy['django']['databases']['engine'],
        'NAME': config_secret_deploy['django']['databases']['name'],
        'USER': config_secret_deploy['django']['databases']['user'],
        'PASSWORD': config_secret_deploy['django']['databases']['password'],
        'HOST': config_secret_deploy['django']['databases']['host'],
        'PORT': config_secret_deploy['django']['databases']['port']
    }
}

# CELERY
# CELERY_BROKER_URL = '{}:{}'.format(
#     config_secret_deploy['django']['celery']['broker_url'],
#     config_secret_deploy['django']['celery']['broker_port']
# )
# CELERY_RESULT_BACKEND = '{}:{}'.format(
#     config_secret_deploy['django']['celery']['broker_url'],
#     config_secret_deploy['django']['celery']['broker_port']
# )

print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)

CORS_ORIGIN_ALLOW_ALL = True

