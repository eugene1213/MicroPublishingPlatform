from django.conf.urls import url, include

from column.apis import PostCreateView, TempCreateView, PostBuy, PostLikeToggleView, PostView
from column.apis.post import PostListView
from column.apis.tmp import TempListView, TempFileUpload


urlpatterns = [
    # 포스트 생성
    url(r'^post-create/$', PostCreateView.as_view(), name='post-create'),
    url(r'^post-like/$', PostLikeToggleView.as_view(), name='buy'),
    url(r'^post-buy/$', PostBuy.as_view(), name='post-like'),
    url(r'^post-view/$', PostView.as_view(), name='post-view'),
    url(r'^postList/', include([
            url(r'^$', PostListView.as_view(), name="post-list"),
            url(r'^(?P<page>\w+)$', PostListView.as_view(), name="post-list-page")
    ])),


    # 임시저장
    url(r'^temp/$', TempCreateView.as_view(), name='post-create'),
    url(r'^temp-list/$', TempListView.as_view(), name='temp'),
    url(r'^tmpimageupload/$', TempFileUpload.as_view(), name='image-upload'),

    # url(r'^login/$', apis.PostLikeToggleView.as_view(), name='login'),
]
