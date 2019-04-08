from functools import wraps
from django.http import HttpResponseBadRequest

def ajax_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    return wrapper
