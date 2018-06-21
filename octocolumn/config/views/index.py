import re

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from column.models import Post
from member.models import User, BuyList
from utils.crypto import decode
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
    if request.user.is_authenticated:
            response = render_to_response("view/main.html", {"login": True})
            return response
    return render_to_response("view/main.html", )


def write(request, temp_id=None):
    if request.user.is_authenticated:
            response = render_to_response("view/write.html", {"login": True})
            return response
    return redirect('views:index')


def read(request, author=None, title=None):
    def url_exchange(title):
        url = re.sub('[/~₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|,|\.|\/|<|>|\?/g]', '', title)
        return url.replace(' ', '-')

    def author_exchange(author):
        url = re.sub('[/~₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|,|\.|\/|<|>|\?/g]', '', author)
        return url.replace(' ', '')

    post_num = title.split('-')
    if len(post_num) is 1:
        raise Http404

    if not int(post_num[-1]) % 1 == 0:
        raise Http404

    try:
        post = Post.objects.filter(pk=int(post_num[-1])).get()

        if post.price == 0:
            if request.user.is_authenticated:
                response = render_to_response("view/read.html", {
                    "login": True,
                    "title": post.title,
                    "cover_image": post.cover_image,
                    "url": 'https://bycal.co/' + '@' + author_exchange(post.author.nickname) + '/' +
                           url_exchange(post.title) +
                           "-" + str(post.pk),

                })
                return response
            response = render_to_response("view/read.html", {
                "login": False,
                "title": post.title,
                "cover_image": post.cover_image,
                "url": 'https://bycal.co/' + '@' + author_exchange(post.author.nickname) + '/' +
                       url_exchange(post.title) +
                       "-" + str(post.pk),
            })
            return response

        else:
            if request.user.is_authenticated:
                response = render_to_response("view/read.html", {
                    "login": True,
                    "title": post.title,
                    "cover_image": post.cover_image,
                    "url": 'https://bycal.co/preview/' + '@' + author_exchange(post.author.nickname) + '/' +
                           url_exchange(post.title) +
                           "-" + str(post.pk),
                })
                return response
            return redirect('views:index')

    except ObjectDoesNotExist:
        raise Http404


def preview(request, author=None, title=None):
    token = request.COOKIES.get('token')

    def main_content(obj):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', obj)
        return clean_text[:100]

    # 특수문자 처리
    def url_exchange(title):
        url = re.sub('[/~₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|,|\.|\/|<|>|\?/g]', '', title)
        return url.replace(' ', '-')

    def author_exchange(author):
        url = re.sub('[/~₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|,|\.|\/|<|>|\?/g]', '', author)
        return url.replace(' ', '')

    if request.user.is_authenticated:
        post_num = title.split('-')
        if len(post_num) is 1:
            raise Http404

        if not int(post_num[-1]) % 1 == 0:
            raise Http404

        try:
            post = Post.objects.filter(pk=int(post_num[-1])).get()
            response = render_to_response("view/preview.html", {
                "login": True,
                "title": post.title,
                "main_content": main_content(post.main_content),
                "cover_image": post.cover_image,
                "url": 'https://bycal.co/preview/' + '@' + author_exchange(post.author.nickname) + '/' +
                       url_exchange(post.title) +
                       "-" + str(post.pk),
                "preview": post.preview,
                "created_datetime": post.created_date.strftime('%Y.%m.%d') + ' ' + post.created_date.strftime('%H:%M'),
                "username": post.author.nickname
            })
            return response
        except ObjectDoesNotExist:
            raise Http404
    else:
        post_num = title.split('-')
        if len(post_num) is 1:
            raise Http404

        if not int(post_num[-1]) % 1 == 0:
            raise Http404

        try:
            post = Post.objects.filter(pk=int(post_num[-1])).get()
            response = render_to_response("view/preview.html", {
                "login": False,
                "title": post.title,
                "main_content": main_content(post.main_content),
                "cover_image": post.cover_image,
                "url": 'https://bycal.co/preview/'+'@' + author_exchange(post.author.nickname) + '/' +
                       url_exchange(post.title) + "-" +
                str(post.pk),
                "preview": post.preview,
                "created_datetime": post.created_date.strftime('%Y.%m.%d') + ' ' + post.created_date.strftime('%H:%M'),
                "username": post.author.nickname
                                                                })
            return response
        except ObjectDoesNotExist:
            raise Http404


def profile(request, member_id=None):
    decode_pk = int(decode(enc=str(member_id)))

    if request.user.is_authenticated:
        try:
            member = User.objects.filter(pk=decode_pk).get()
            if request.user == member:
                response = render_to_response("view/profile.html", {
                    "login": True,
                    "is_user": True
                })
                return response
            response = render_to_response("view/profile.html", {
                "login": True,
                "is_user": False
            })
            return response
        except ObjectDoesNotExist:

            response = render_to_response("view/profile.html", {
                "login": True,
                "is_user": False
            })
            return response
    response = render_to_response("view/profile.html", {
        "login": False,
        "is_user": False
    })
    return response


def more(request, type=None):
    # print(request.user.is_authenticated)
    if request.user.is_authenticated:
        response = render_to_response("view/recent-more.html", {"login": True})
        return response
    response = render_to_response("view/recent-more.html")
    return response


def bookmark(request):
    if request.user.is_authenticated:
        response = render_to_response("view/bookmark.html", {"login": True})
        return response
    return redirect('views:index')


def buylist(request):
    if request.user.is_authenticated:
        response = render_to_response("view/purchased-post.html", {"login": True})
        return response
    return redirect('views:index')


def feed(request):
    if request.user.is_authenticated:
        response = render_to_response("view/feed.html", {"login": True})
        return response
    return redirect('views:index')


# def signin(request):
#
#     if request.COOKIES:
#         token = request.COOKIES.get('token')
#         if token is not None:
#             return redirect('views:index')
#         response = render_to_response("view/beta-signin.html", {"login": False})
#         return response
#     response = render_to_response("view/beta-signin.html", {"login": False})
#     return response


# def signup(request):
#     return render_to_response('view/beta-signup.html')
#
#
# def signinForm(request):
#     return render_to_response('view/beta-signin2.html')
#
#
# def okay(request):
#     return render_to_response('view/beta-okay.html')


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

def naver_request(request):
    return render_to_response('naverd45c8d580806584cb434be95a432581b.html')


def sitemap(request):
    return render_to_response('sitemap.xml')


def robot(request):
    return render_to_response('robots.txt')

