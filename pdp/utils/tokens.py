# coding: utf-8

from django.http import HttpResponse
from django.utils.decorators import available_attrs

from hashlib import md5
from time import time
from functools import wraps

def generate_token():
    return md5('lcdldses?nas. %s salt' % time()).hexdigest()[:12]

def get_token(request):
    return {'get_token': request.session.get('get_token')}

def token_protected(function=None, arg_name='token'):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            provided_key = kwargs.get(arg_name)
            if provided_key is None or get_token(request)['get_token'] != provided_key:
                return HttpResponse(u'Mauvaise clé de session')
            return view_fun(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
