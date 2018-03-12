from django.conf.urls import url, include

from column.apis import PostCreateView, TempCreateView, PostBuy, PostLikeToggleView, PostReadView, AuthorResult, \
    CommentListView, CommentCreateView, IsBuyPost, PostListView, TempListView, TempFileUpload, PostPreReadView, \
    CommentLikeToggleView

urlpatterns = [
    # 포스트 생성
    url(r'^post-create/$', PostCreateView.as_view(), name='post-create'),
    # 포스트 라이트
    url(r'^post-like/$', PostLikeToggleView.as_view(), name='buy'),
    # 포스트 구매
    url(r'^post-buy/$', PostBuy.as_view(), name='post-like'),
    # 포스트 읽기
    url(r'^post-view/(?P<pk>\d+)$', PostReadView.as_view(), name='post-view'),
    # 포스트 프리뷰
    url(r'^post-preview/$', PostPreReadView.as_view(), name='post-view'),

    # 포스트 리스트
    url(r'^postList/', include([
            url(r'^$', PostListView.as_view(), name="post-list"),
            url(r'^(?P<page>\w+)$', PostListView.as_view(), name="post-list-page")
    ])),
    url(r'^post-isbuy/(?P<pk>\d+)$', IsBuyPost.as_view(), name='post-isbuy'),

    # 작가 구분
    url(r'^isauthor/$', AuthorResult.as_view(), name='post-view'),

    # 코멘트 관련
    url(r'^(?P<post_pk>\d+)/commentList/$', CommentListView.as_view(), name='comment-view'),
    url(r'^comment-create/$', CommentCreateView.as_view(), name='comment-create-view'),
    url(r'^(?P<comment_pk>\d+)/comment-like/$', CommentLikeToggleView.as_view(), name='comment-create-view'),

    # 임시저장
    url(r'^temp/$', TempCreateView.as_view(), name='post-create'),
    url(r'^temp-list/$', TempListView.as_view(), name='temp'),
    url(r'^tmpimageupload/$', TempFileUpload.as_view(), name='image-upload'),

    # url(r'^login/$', apis.PostLikeToggleView.as_view(), name='login'),
]
