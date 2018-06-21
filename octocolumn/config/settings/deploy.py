# deploy.py
from .base import *


config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# 배포모드니까 DEBUG는 False
DEBUG = False
ALLOWED_HOSTS = ['bycal.co', '*.bycal.co']
# ALLOWED_HOSTS = '*'


# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'config.middleware.AuthenticationMiddlewareJWT',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Application definition
INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'storages',

    'corsheaders',

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

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config_secret_debug['django']['email']['host']
# EMAIL_HOST_USER = config_secret_debug['django']['email']['host_user']
# EMAIL_HOST_PASSWORD = config_secret_debug['django']['email']['host_password']
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'azure_3d95bc9766fc6c1c425b6283d64a5593@azure.com'
EMAIL_HOST_PASSWORD = '!devocto1234'
EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'yourfriends@bycal.co'

# AWS settings
# AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
# AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']
# AWS_STORAGE_BUCKET_NAME = config_secret_deploy['aws']['s3_bucket_name']
# AWS_S3_REGION_NAME = config_secret_deploy['aws']['s3_region_name']
# AWS_QUERYSTRING_AUTH = False
# AWS_CLOUDFRONT_DOMAIN = 'static.octocolumn.com'
# AWS_HEADERS = {'Cache-Control': 'max-age=86400', }
#
# S3_USE_SIGV4 = True
#
# AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_S3_REGION_NAME
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Azure settings
AZURE_STORAGE_ACCOUNT = config_secret_deploy['azure']['account']
AZURE_STORAGE_KEY = config_secret_deploy['azure']['account_key']

## AZURE Static Setting
STATICFILES_STORAGE = 'config.s3storages.AzureStaticStorage'
STATICFILES_LOCATION = 'static'
# STATIC_URL = 'https://{account}.azureedge.net/{mediafiles_location}/'.format(
#                 account=AZURE_STORAGE_ACCOUNT,
#                 mediafiles_location=STATICFILES_LOCATION
# )
STATIC_URL = 'https://bycal.blob.core.windows.net/static/'

# AWS Static Settings
# STATICFILES_STORAGE = 'config.s3storages.StaticStorage'
# STATICFILES_LOCATION = 'static'
# STATIC_URL = 'https://{custom_domain}/{staticfiles_location}/'.format(
#         custom_domain=AWS_CLOUDFRONT_DOMAIN,
#         staticfiles_location=STATICFILES_LOCATION,
#     )

STATIC_ROOT = STATIC_URL

# base static
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'

## AZURE Media settigns
DEFAULT_FILE_STORAGE = 'config.s3storages.AzureMediaStorage'
MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = 'https://{account}.azureedge.net/{mediafiles_location}/'.format(
#                 account=AZURE_STORAGE_ACCOUNT,
#                 mediafiles_location=MEDIAFILES_LOCATION
# )

MEDIA_URL = 'https://bycal.blob.core.windows.net/media/'


## AWS Media Setting
# DEFAULT_FILE_STORAGE = 'config.s3storages.MediaStorage'
# MEDIAFILES_LOCATION = 'media'
#
# MEDIA_URL = 'https://{custom_domain}/{mediafiles_location}/'.format(
#     custom_domain=AWS_CLOUDFRONT_DOMAIN,
#     mediafiles_location=MEDIAFILES_LOCATION,
# )

MEDIA_ROOT = MEDIA_URL

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

# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': [
#             "octocolumn-001.rqgefq.0001.apn2.cache.amazonaws.com:6379",
#             "octocolumn-002.rqgefq.0001.apn2.cache.amazonaws.com:6379",
#             "octocolumn-003.rqgefq.0001.apn2.cache.amazonaws.com:6379"
#         ],
#         'OPTIONS': {
#             'DB': 1,
#             'MASTER_CACHE': "octocolumn-001.rqgefq.0001.apn2.cache.amazonaws.com:6379"
#         },
#     },
# }
# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',

# CELERY
# CELERY_BROKER_URL = '{}:{}'.format(
#     config_secret_deploy['django']['celery']['broker_url'],
#     config_secret_deploy['django']['celery']['broker_port']
# )
# CELERY_RESULT_BACKEND = '{}:{}'.format(
#     config_secret_deploy['django']['celery']['broker_url'],
#     config_secret_deploy['django']['celery']['broker_port']
# )

# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': 'bycal.redis.cache.windows.net:6380',
#         'OPTIONS': {
#             "PASSWORD": "XNv66F+JWKzeJdD+mYs9wvhlcKbs2Ax95pJ+HXpX4NQ=",
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # 'DB': 1,
#         },
#     },
# }

CELERY_BROKER_URL = 'amqp://bycal:Devocto12345678@52.231.67.49:5672//'


# Google
CLIENT_ID = config_secret_deploy['accounts']['google']['client_id']
CLIENT_SECRET = config_secret_deploy['accounts']['google']['client_secret']
REDIRECT_URI = config_secret_deploy['accounts']['google']['javascript_origins']
AUTH_URI = config_secret_deploy['accounts']['google']['auth_uri']
TOKEN_URI = config_secret_deploy['accounts']['google']['token_uri']

print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)

#
# ERROR_DIR = os.path.join(ROOT_DIR, '.error_log')
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters':
#         {
#             'verbose':
#               {
#                   'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#                   'datefmt' : "%d/%b/%Y %H:%M:%S"
#               },
#             'simple':
#                 {
#                     'format': '%(levelname)s %(message)s'
#                 },
#         },
#     'handlers':
#         {
#             'file':
#                 {
#                     'level': 'DEBUG',
#                     'class': 'logging.handlers.RotatingFileHandler',
#                     'filename': os.path.join(ERROR_DIR, 'debug.txt'),
#                     'formatter': 'verbose',
#                     'maxBytes': 1024*1024*10, 'backupCount': 5,
#                 },
#         },
#     'loggers':
#         {
#             'django':
#                 {
#                     'handlers': ['file'],
#                     'propagate': True,
#                     'level':'INFO',
#                 },
#             'django.request':
#                 {
#                     'handlers':['file'],
#                     'propagate': False,
#                     'level':'INFO',
#                 },
#             'myAppName':
#                 {
#                     'handlers': ['file'],
#                     'level': 'DEBUG',
#                 },
#         }
# }

JET_SIDE_MENU_COMPACT = True
#
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#
# SECURE_HSTS_SECONDS = 31536000
#
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

CORS_ORIGIN_ALLOW_ALL = True

SITE_ID = 1

