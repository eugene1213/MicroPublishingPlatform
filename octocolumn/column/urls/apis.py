from django.conf.urls import url

from column.apis import PostCreateView, TempCreateView, PostBuy
from column.apis.tmp import TempListView, TempFileUpload

urlpatterns = [
    url(r'^postcreate/$', PostCreateView.as_view(), name='postcreate'),
    url(r'^temp/$', TempCreateView.as_view(), name='postcreate'),
    url(r'^templist/$', TempListView.as_view(), name='temp'),
    url(r'^tmpimageupload/$', TempFileUpload.as_view(), name='imageupload'),
    url(r'^buy/$', PostBuy.as_view(), name='buy'),

    # url(r'^login/$', apis.PostLikeToggleView.as_view(), name='login'),
]
