from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import apis

urlpatterns = [
    # url(r'^', include(views)),
    url(r'^api/', include(apis, namespace='api')),
    url(r'^api-test/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
