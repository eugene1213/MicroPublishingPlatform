from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True


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



