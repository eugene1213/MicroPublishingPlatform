from django.conf.urls import url, include
from django.contrib import admin

from config.views import index
from config.views.index import write, kakao, google, facebook, recent, signin, signup, signinForm, okay
from config.views.index import read
from config.views.index import profile
from member.apis import VerifyEmail, PasswordResetEmail

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^write/', include([
            url(r'^$', write, name="write"),
            url(r'^(?P<temp_id>\d+)$', write, name="temp_write")
    ]), name='write'),
    url(r'^read/(?P<post_id>\d+)$', read, name='read'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^recent/$', recent, name='recent'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signinForm/$', signinForm, name='signinForm'),
    url(r'^okay/$', okay, name='okay'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^kakao-login/$', kakao, name='kakao-login'),
    url(r'^google-login/$', google, name='google-login'),
    url(r'^facebook-login/$', facebook, name='google-login'),

    # 이메일 체킹
    url(r'^verifyChecking/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        VerifyEmail.as_view(), name='verifyChecking'),

    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetEmail.as_view(), name='password-reset'),

    url(r'^inviteChecking/(?P<uidb64>[0-9A-Za-z_\-]+)//(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetEmail.as_view(), name='password-reset'),

]
