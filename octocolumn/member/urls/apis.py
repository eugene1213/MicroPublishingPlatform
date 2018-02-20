from django.conf.urls import url

from member import apis
from member.apis import Login, SignUp, FacebookLogin, ValidationSecondPassword, SecondPasswordCreateView, Logout, \
    GoogleLogin

urlpatterns = [
    # api:member:login
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^signup/$',SignUp.as_view(), name='signup'),
    url(r'^facebook-login/', FacebookLogin.as_view(), name='facebook'),

    url(r'^google-login/', GoogleLogin.as_view(), name='google'),
    # url(r'^facebook-login/', apis.FacebookLogin.as_view()),


    # api:author 신청
    url(r'^author-apply', apis.AuthorAplly.as_view(),name='apply'),

    # 2차 비밀번호 관련
    url(r'^create-sp', SecondPasswordCreateView.as_view(), name='create-sp'),
    url(r'^validation-sp', ValidationSecondPassword.as_view(), name='validation-sp')

]
