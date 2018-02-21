from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from member.apis.verify import VerifyEmail
from . import apis

urlpatterns = [
    # url(r'^', include(views)),
    url(r'^api/', include(apis, namespace='api')),
    url(r'^api-test/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^verifyChecking/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        VerifyEmail.as_view(), name='verifyChecking'),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
