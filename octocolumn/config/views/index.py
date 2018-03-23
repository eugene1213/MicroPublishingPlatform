import re

from django.shortcuts import render_to_response, redirect
from django.views.decorators.cache import never_cache

__all__ = (
    'index',
)


def mobile(request):

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

@never_cache
def index(request):
    if mobile(request):
        return render_to_response('mobile/main_m.html', )

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/main.html", {"login": True})
            return response
        return render_to_response('view/main.html', )
    return render_to_response('view/main.html',)


@never_cache
def write(request, temp_id=None):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/write.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')


@never_cache
def read(request, post_id=None):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/read.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')

@never_cache
def profile(request):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/profile.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')


def recent(request):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/recent-more.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')


@never_cache
def signin(request):

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            return redirect('views:index')
        response = render_to_response("view/beta-signin.html", {"login": False})
        return response
    response = render_to_response("view/beta-signin.html", {"login": False})
    return response


@never_cache
def signup(request):
    return render_to_response('view/beta-signup.html')


@never_cache
def signinForm(request):
    return render_to_response('view/beta-signin2.html')


@never_cache
def okay(request):
    return render_to_response('view/beta-okay.html')


@never_cache
def facebook(request):
    return render_to_response('view/login/facebook_login.html')


@never_cache
def kakao(request):
    return render_to_response('view/login/kakao_login.html')


@never_cache
def google(reqeust):
    return render_to_response('view/login/google_login.html')


