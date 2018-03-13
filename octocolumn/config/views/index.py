from django.contrib.auth.middleware import get_user
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from column.models import Post
from member.models import BuyList

__all__ = (
    'index',
)


def index(request):
    if request.COOKIES:
        response = render_to_response("view/main.html", {"login": True})
        return response
        return render_to_response('view/main.html',)
    return render_to_response('view/main.html',)

def write(request):
    if request.COOKIES:
        response = render_to_response("view/write.html", {"login": True})
        return response
    return render_to_response('view/main.html')


def read(request, post_id):

    if request.COOKIES:
        response = render_to_response("view/read.html", {"login": True})
        return response
    return render_to_response('view/main.html')


def profile(request):
    if request.COOKIES:
        response = render_to_response("view/profile.html", {"login": True})
        return response
    return render_to_response('view/main.html')

def facebook(request):
    return render_to_response('view/login/facebook_login.html')


def kakao(request):
    return render_to_response('view/login/kakao_login.html')


def google(reqeust):
    return render_to_response('view/login/google_login.html')
