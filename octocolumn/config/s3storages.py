import re

from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from storages.backends.s3boto import S3BotoStorage


# class StaticStorage(S3BotoStorage):
#     location = settings.STATICFILES_LOCATION
#     file_overwrite = True
#
#     def __init__(self, *args, **kwargs):
#         kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
#         super(StaticStorage, self).__init__(*args, **kwargs)
#
#
# class MediaStorage(S3BotoStorage):
#     location = settings.MEDIAFILES_LOCATION
#     file_overwrite = True
#
#     def __init__(self, *args, **kwargs):
#         kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
#         super(MediaStorage, self).__init__(*args, **kwargs)


class AzureStaticStorage(AzureStorage):
    account_name = settings.AZURE_STORAGE_ACCOUNT
    account_key = settings.AZURE_STORAGE_KEY
    azure_container = 'static'
    file_overwrite = True


# class AzureMediaStorage(AzureStorage):
#     account_name = settings.AZURE_STORAGE_ACCOUNT
#     account_key = settings.AZURE_STORAGE_KEY
#     azure_container = 'media'
#     file_overwrite = True

# class AzureStaticStorage(AzureStorage):
#
#     def url(self, name):
#         ret = super(AzureStaticStorage, self).url(name)
#         _ret = re.sub('//[a-z.0-9A-Z]*/', settings.STATIC_URL, ret)
#         return _ret

class AzureMediaStorage(AzureStorage):

    def url(self, name):
        ret = super(AzureMediaStorage, self).url(name)
        _ret = re.sub('//[a-z.0-9A-Z]*/', settings.MEDIA_URL, ret)
        return _ret

