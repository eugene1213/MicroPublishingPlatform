from django.shortcuts import render_to_response
from django.template import RequestContext

__all__ = (
    'index',
)


def index(request):
    print(request.COOKIES)
    if request.COOKIES is not None:
        if request.COOKIES['token']:
            response = render_to_response("view/main.html", {"login": True})
            return response
        return render_to_response('view/main.html',)
    return render_to_response('view/main.html',)

def write(request):
    return render_to_response('view/write.html')

def read(request):
    return render_to_response('view/read.html')