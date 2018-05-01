from django.shortcuts import render_to_response


def index(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/about.html", {"login": True})
            return response
        return render_to_response("support/about.html", )
    return render_to_response("support/about.html",)


def staff_blog(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/staff_blog.html", {"login": True})
            return response
        return render_to_response("support/staff_blog.html", )
    return render_to_response("support/staff_blog.html",)


def contact(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/contact.html", {"login": True})
            return response
        return render_to_response("support/contact.html", )
    return render_to_response("support/contact.html",)


def help_octo(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/help-1.html", {"login": True})
            return response
        return render_to_response("support/help-1.html", )
    return render_to_response("support/help-1.html",)


def notice(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/notice.html", {"login": True})
            return response
        return render_to_response("support/notice.html", )
    return render_to_response("support/notice.html",)


def policies(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/policies.html", {"login": True})
            return response
        return render_to_response("support/policies.html", )
    return render_to_response("support/policies.html",)


def jobs(request):
    if request.COOKIES:
        token = request.COOKIES.get('token')
        if token is not None:
            response = render_to_response("support/jobs.html", {"login": True})
            return response
        return render_to_response("support/jobs.html", )
    return render_to_response("support/jobs.html",)
