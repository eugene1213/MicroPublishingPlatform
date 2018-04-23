import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache

from column.models import Post
from member.models import User
from utils.tokengenerator import account_activation_token

__all__ = (
    'index',
    'handler404',
    'handler500'

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
        return render_to_response("view/main.html", )
    return render_to_response("view/main.html",)


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


def read(request, author=None, title=None):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:

            post_num = title.split('-')
            if len(post_num) is 1:
                raise Http404

            if not int(post_num[-1]) % 1 == 0:
                raise Http404

            try:
                Post.objects.filter(pk=int(post_num[-1])).get()
                response = render_to_response("view/read.html", {"login": True})
                return response

            except ObjectDoesNotExist:
                raise Http404
        return redirect('views:index')
    # return redirect('views:index')


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


def bookmark(request):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/bookmark.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')


def buylist(request):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/purchased-post.html", {"login": True})
            return response
        return redirect('views:index')
    return redirect('views:index')


def feed(request):
    if mobile(request):
        return redirect('views:index')

    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/feed.html", {"login": True})
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


def findPass(request):
    return render_to_response('view/beta-findPass.html')


def resetPass(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return render_to_response('view/resetPass.html')
    else:
        return HttpResponseRedirect(redirect_to='/')


def shop(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("view/shop.html", {"login": True})
            return response
        return render_to_response("view/shop.html", )
    return render_to_response("view/shop.html",)


def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('404.html')
    response.status_code = 500
    return response


@never_cache
def facebook(request):
    return render_to_response('view/login/facebook_login.html')


@never_cache
def kakao(request):
    return render_to_response('view/login/kakao_login.html')


@never_cache
def google(reqeust):
    return render_to_response('view/login/google_login.html')


@never_cache
def naver_request(request):
    return render_to_response('naver6bc332ab9aa51989a598805bc6c439d3.html')
