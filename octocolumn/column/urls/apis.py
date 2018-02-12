from django.conf.urls import url

from column.apis import PostCreateView, TempCreateView, PostBuy, PostLikeToggleView
from column.apis.tmp import TempListView, TempFileUpload


urlpatterns = [
    # 포스트 생성
    url(r'^postcreate/$', PostCreateView.as_view(), name='post-create'),
    url(r'^postlike/$', PostLikeToggleView.as_view(), name='buy'),
    url(r'^buy/$', PostBuy.as_view(), name='post-like'),

    # 임시저장
    url(r'^temp/$', TempCreateView.as_view(), name='post-create'),
    url(r'^templist/$', TempListView.as_view(), name='temp'),
    url(r'^tmpimageupload/$', TempFileUpload.as_view(), name='image-upload'),

    # url(r'^login/$', apis.PostLikeToggleView.as_view(), name='login'),
]
