from django.conf.urls import url, include
from django.contrib import admin

from config.views import index
from member.apis.verify import VerifyEmail, PasswordResetEmail

urlpatterns = [
    url(r'^$', index, name='index'),

    # url(r'^post/', include('column.urls.views', namespace='post')),
    url(r'^member/', include('member.urls.views', namespace='member')),
    #

]
