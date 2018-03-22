# deploy.py
from .base import *


config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# 배포모드니까 DEBUG는 False
DEBUG = False
ALLOWED_HOSTS = ['octocolumn.com', 'www.octocolumn.com', 'm.octocolumn.com']


# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
    'storages',

    # 장고 접속 에이전트 체크 라이브러리
    'django_user_agents',
    'django_s3_storage',
    # 'azure',

    'ipware',

    'rest_framework',
    'rest_framework.authtoken',

    'member',
    'column',
    'octo'

]

# AWS settings
AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret_deploy['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = config_secret_deploy['aws']['s3_region_name']
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {'Cache-Control': 'max-age=86400', }

S3_USE_SIGV4 = True

AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_S3_REGION_NAME
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Azure settings
# AZURE_STORAGE_ACCOUNT = config_secret_deploy['azure']['account']
# AZURE_STORAGE_KEY = config_secret_deploy['azure']['account_key']

## AZURE Static Setting
# STATICFILES_STORAGE = 'config.s3storages.AzureStaticStorage'
# STATICFILES_LOCATION = 'static'
# STATIC_URL = 'http://{account}.blob.core.windows.net/{staticfiles_location}/'.format(
#                 account=AZURE_STORAGE_ACCOUNT,
#                 staticfiles_location=STATICFILES_LOCATION
# )


# AWS Static Settings
STATICFILES_STORAGE = 'config.s3storages.StaticStorage'
STATICFILES_LOCATION = 'static'
STATIC_URL = 'https://{custom_domain}/{staticfiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        staticfiles_location=STATICFILES_LOCATION,
    )
# base static
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'

## AZURE Media settigns
# DEFAULT_FILE_STORAGE = 'config.s3storages.AzureMediaStorage'
# MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = 'http://{account}.blob.core.windows.net/{mediafiles_location}/'.format(
#                 account=AZURE_STORAGE_ACCOUNT,
#                 mediafiles_location=STATICFILES_LOCATION
# )

## AWS Media Setting
DEFAULT_FILE_STORAGE = 'config.s3storages.MediaStorage'
MEDIAFILES_LOCATION = 'media'

MEDIA_URL = 'https://{custom_domain}/{mediafiles_location}/'.format(
    custom_domain=AWS_S3_CUSTOM_DOMAIN,
    mediafiles_location=MEDIAFILES_LOCATION,
)


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

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            "octocolumn-001.rqgefq.0001.apn2.cache.amazonaws.com:6379",
            "octocolumn-002.rqgefq.0001.apn2.cache.amazonaws.com:6379",
            "octocolumn-003.rqgefq.0001.apn2.cache.amazonaws.com:6379"
        ],
        'OPTIONS': {
            'DB': 1,
            'MASTER_CACHE': "octocolumn-001.rqgefq.0001.apn2.cache.amazonaws.com:6379"
        },
    },
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


ERROR_DIR = os.path.join(ROOT_DIR, '.error_log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':
        {
            'verbose':
              {
                  'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                  'datefmt' : "%d/%b/%Y %H:%M:%S"
              },
            'simple':
                {
                    'format': '%(levelname)s %(message)s'
                },
        },
    'handlers':
        {
            'file':
                {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(ERROR_DIR, 'debug.txt'),
                    'formatter': 'verbose',
                    'maxBytes': 1024*1024*10, 'backupCount': 5,
                },
        },
    'loggers':
        {
            'django':
                {
                    'handlers': ['file'],
                    'propagate': True,
                    'level':'INFO',
                },
            'django.request':
                {
                    'handlers':['file'],
                    'propagate': False,
                    'level':'INFO',
                },
            'myAppName':
                {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                },
        }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

CORS_ORIGIN_ALLOW_ALL = True

SITE_ID = 1
