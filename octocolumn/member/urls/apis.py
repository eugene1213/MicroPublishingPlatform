from django.conf.urls import url

from member import apis
from member.apis import Login, SignUp, FacebookLogin

urlpatterns = [
    # api:member:login
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$',SignUp.as_view(), name='signup'),
    url(r'^facebook-login/', FacebookLogin.as_view(),name='facebook'),
    # url(r'^google-login/', apis.FacebookLogin.as_view()),
    # url(r'^facebook-login/', apis.FacebookLogin.as_view()),

    # api:author 신청
    url(r'^author-apply', apis.AuthorAplly.as_view(),name='apply')
]
