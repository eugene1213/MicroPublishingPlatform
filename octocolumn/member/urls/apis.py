from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token

from member import apis
from member.apis import Login, SignUp, FacebookLogin, ValidationSecondPassword, SecondPasswordCreateView, Logout, \
    GoogleLogin, UpdatePassword, Follower, UserInfo, KakaoLogin, UserCoverImageUpload, ProfileImageUpload


urlpatterns = [
    # api:member:login
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^signup/$',SignUp.as_view(), name='signup'),
    url(r'^password-change/$', UpdatePassword.as_view(), name='password-change'),
    url(r'^userInfo/$', UserInfo.as_view(), name='signup'),

    # 토큰 관련
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-auth/', obtain_jwt_token),


    url(r'^facebook-login/', FacebookLogin.as_view(), name='facebook'),
    url(r'^google-login/(?P<token>.*)$', GoogleLogin.as_view(), name='google'),
    url(r'^kakao-login/(?P<token>.*)$', KakaoLogin.as_view(), name='kakao'),


    # 프로필 관련
    url(r'^profile-image/', ProfileImageUpload.as_view(), name='facebook'),
    url(r'^usercover-image/', UserCoverImageUpload.as_view(), name='facebook'),

    # follower
    url(r'^(?P<user_pk>\d+)/follow/$', Follower.as_view(), name='facebook'),

    # api:author 신청
    url(r'^author-apply', apis.AuthorAplly.as_view(), name='apply'),

    # 2차 비밀번호 관련
    url(r'^create-sp', SecondPasswordCreateView.as_view(), name='create-sp'),
    url(r'^validation-sp', ValidationSecondPassword.as_view(), name='validation-sp')

]
