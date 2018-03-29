from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(StaticStorage, self).__init__(*args, **kwargs)


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)







# class AzureStaticStorage(AzureStorage):
#     account_name = settings.AZURE_STORAGE_ACCOUNT
#     account_key = settings.AZURE_STORAGE_KEY
#     azure_container = 'static'
#     file_overwrite = True
#
#
#
# class AzureMediaStorage(AzureStorage):
#     account_name = settings.AZURE_STORAGE_ACCOUNT
#     account_key = settings.AZURE_STORAGE_KEY
#     azure_container = 'media'
#     file_overwrite = True



