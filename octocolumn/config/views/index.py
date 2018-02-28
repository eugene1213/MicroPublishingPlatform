from django.shortcuts import render_to_response

__all__ = (
    'index',
)


def index(request):
    return render_to_response('view/main.html')

def write(request):
    return render_to_response('view/write.html')