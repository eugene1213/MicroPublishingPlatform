from django.conf.urls import url, include

urlpatterns = [
    url(r'^member/', include('member.urls.apis', namespace='member')),
    url(r'^column/', include('column.urls.apis', namespace='column')),

    # url(r'^sms/', include('sms.urls', namespace='sms')),
]
