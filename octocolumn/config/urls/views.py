from django.conf.urls import url, include
from django.contrib import admin

from config.views import index
from config.views.index import write, kakao, google, facebook
from config.views.index import read
from config.views.index import profile
from member.apis.verify import VerifyEmail, PasswordResetEmail

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^write/$',write, name='write'),
    url(r'^read/(?P<post_id>\d+)$', read, name='read'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^kakao-login/$', kakao, name='kakao-login'),
    url(r'^google-login/$', google, name='google-login'),
    url(r'^facebook-login/$', facebook, name='google-login'),

    # url(r'^post/', include('column.urls.views', namespace='post')),

]
