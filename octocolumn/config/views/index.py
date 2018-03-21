import re

from django.shortcuts import render_to_response, redirect

__all__ = (
    'index',
)


def mobile(request):

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


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
    response = render_to_response("view/recent-more.html", {"login": False})
    return response


def signin(request):

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            return redirect('views:index')
        response = render_to_response("view/beta-signin.html", {"login": False})
        return response
    response = render_to_response("view/beta-signin.html", {"login": False})
    return response


def signup(request):
    return render_to_response('view/beta-signup.html')

def signinForm(request):
    return render_to_response('view/beta-signin2.html')

def okay(request):
    return render_to_response('view/beta-okay.html')

def facebook(request):
    return render_to_response('view/login/facebook_login.html')


def kakao(request):
    return render_to_response('view/login/kakao_login.html')


def google(reqeust):
    return render_to_response('view/login/google_login.html')


