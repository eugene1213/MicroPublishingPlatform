from django.contrib.auth.middleware import get_user
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from column.models import Post
from member.models import BuyList
from member.models.user import Relation

__all__ = (
    'index',
)


def index(request):
    if request.COOKIES:
        try:
            request.COOKIES.get('token')
            response = render_to_response("view/main.html", {"login": True})
            return response
        except ObjectDoesNotExist:
            return render_to_response('view/main.html', )
    return render_to_response('view/main.html',)


def write(request):
    if request.COOKIES:
        try:
            request.COOKIES.get('token')
            response = render_to_response("view/write.html", {"login": True})
            return response
        except ObjectDoesNotExist:
            return render_to_response('view/main.html', )
    return render_to_response('view/main.html', )


def read(request, post_id):

    if request.COOKIES:
        try:
            request.COOKIES.get('token')
            response = render_to_response("view/read.html", {"login": True})
            return response
        except ObjectDoesNotExist:
            return render_to_response('view/main.html', )
    return render_to_response('view/main.html', )


def profile(request):
    if request.COOKIES:
        try:
            request.COOKIES.get('token')
            response = render_to_response("view/profile.html", {"login": True})
            return response
        except ObjectDoesNotExist:
            return render_to_response('view/main.html', )
    return render_to_response('view/main.html', )


def facebook(request):
    return render_to_response('view/login/facebook_login.html')


def kakao(request):
    return render_to_response('view/login/kakao_login.html')


def google(reqeust):
    return render_to_response('view/login/google_login.html')


