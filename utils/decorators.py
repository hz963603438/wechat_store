from django.http import JsonResponse


def login_required_ajax(func):
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({"code": -1})

    return _wrapper