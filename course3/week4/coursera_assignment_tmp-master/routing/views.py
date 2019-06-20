from django.http import *


# create views
from django.views.decorators.http import require_POST


def simple_route(request):
    if request.method == 'GET':
        return HttpResponse("")
    else:
        return HttpResponseNotAllowed("<h2>Method is not allowed</h2>")


def slug_route(request, body):
    return HttpResponse(body)


# def sum_route(request, a, b):
#     try:
#         a = int(a)
#         b = int(b)
#     except (ValueError, TypeError):
#         HttpResponseNotFound("<h2>Not Found</h2>")
#     return HttpResponse("{}".format(a + b))


def sum_route(request, a, b):
    try:
        a = int(a)
        b = int(b)
    except (ValueError, TypeError):
        return HttpResponseNotFound("<h2>Not Found</h2>")
        # return HttpResponseBadRequest("<h2>Bad Request</h2>")
    return HttpResponse("{}".format(a + b))


def sum_get_method(request):
    if request.method == 'GET':
        a = request.GET.get("a")
        b = request.GET.get("b")
        try:
            a = int(a)
            b = int(b)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("<h2>Bad Request</h2>")
        return HttpResponse(a + b)
    else:
        return HttpResponseNotAllowed("<h2>Method is not allowed</h2>")


def sum_post_method(request):
    if request.method == 'POST':
        a = request.POST.get("a")
        b = request.POST.get("b")
        try:
            a = int(a)
            b = int(b)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("<h2>Bad Request</h2>")
        return HttpResponse(a + b)
    else:
        return HttpResponseNotAllowed("<h2>Method is not allowed</h2>")