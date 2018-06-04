from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import apis, views

urlpatterns = [
    url(r'^', include(views, namespace='views')),
    url(r'^api/', include(apis, namespace='api')),
    url(r'^morningCoffee/', include(admin.site.urls)),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

]

handler404 = 'config.views.handler404'
handler500 = 'config.views.handler500'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns
