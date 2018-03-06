from django.conf import settings
from django.contrib.auth import (
    logout as django_logout,
)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from ..forms import LoginForm

__all__ = (
    'login',
    'logout',
)

@csrf_exempt
def login(request):
    # GET파라미터의 'next'값을 사용하도록 수정

    # POST요청 (Form submit)의 경우
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            print(request)
            print(request.COOKIES)
            return redirect('views:index')
    else:
        # GET요청에서는 Form을 보여줌
        form = LoginForm()
    context = {
        'login_form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


