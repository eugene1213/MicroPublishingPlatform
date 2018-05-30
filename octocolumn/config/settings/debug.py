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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'config.middleware.AuthenticationMiddlewareJWT',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     # other finders..
#     'compressor.finders.CompressorFinder',
# )

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

    # 디버깅 툴바
    'debug_toolbar',
    'silk',

    # 장고 접속 에이전트 체크 라이브러리
    'django_user_agents',

    # CORS 수정
    'corsheaders',
    # compressor
    # 'compressor',

    # storages
    'storages',

    # rest_framework
    'rest_framework',
    'rest_framework.authtoken',
    'ipware',

    'member',
    'column',
    'octo'

]

# COMPRESS_ENABLED = False
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.cssmin.CSSMinFilter',
#     # 'compressor.filters.jsmin.JSMinFilter'
#     # 'compressor.filters.jsmin.SlimItFilter',
#     # 'compressor.filters.cssmin.CSSCompressorFilter',
#     # 'compressor.parser.Html5LibParser',
# ]

# Email
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config_secret_debug['django']['email']['host']
EMAIL_HOST_USER = config_secret_debug['django']['email']['host_user']
EMAIL_HOST_PASSWORD = config_secret_debug['django']['email']['host_password']
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

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

INTERNAL_IPS = ('127.0.0.1', 'localhost')

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
  ]
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            # "PASSWORD": "!devocto1234",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 'DB': 1,
        },
    },
}

# Storage settings
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
# STATICFILES_STORAGE = 'config.storages.StaticStorage'

FACEBOOK_APP_ID = config_secret_debug['accounts']['facebook']['app_id']
FACEBOOK_APP_SECRET_CODE = config_secret_debug['accounts']['facebook']['secret_code']

# Google
CLIENT_ID = config_secret_debug['accounts']['google']['client_id']
CLIENT_SECRET = config_secret_debug['accounts']['google']['client_secret']
REDIRECT_URI = config_secret_debug['accounts']['google']['javascript_origins']
AUTH_URI = config_secret_debug['accounts']['google']['auth_uri']
TOKEN_URI = config_secret_debug['accounts']['google']['token_uri']


# Celery
# BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# CELERY_BROKER_URL = 'redis://{}:{}'.format(
#     config_secret_debug['django']['celery']['broker_url'],
#     config_secret_debug['django']['celery']['broker_port']
# )
# CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(
#     config_secret_debug['django']['celery']['broker_url'],
#     config_secret_debug['django']['celery']['broker_port']
# )
# print(CELERY_BROKER_URL)
JET_SIDE_MENU_COMPACT = True

print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)

SESSION_COOKIE_HTTPONLY =True

CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_SECURE = False
