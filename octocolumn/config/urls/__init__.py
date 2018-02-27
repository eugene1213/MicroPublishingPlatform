from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from member.apis.verify import VerifyEmail, PasswordResetEmail
from . import apis, views

urlpatterns = [
    url(r'^', include(views, namespace='views')),
    url(r'^api/', include(apis, namespace='api')),
    url(r'^admin/', include(admin.site.urls)),


    # 이메일 체킹
    url(r'^verifyChecking/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        VerifyEmail.as_view(), name='verifyChecking'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetEmail.as_view(), name='password-reset'),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
