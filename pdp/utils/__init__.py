# coding: utf-8

"""Regroups various tools used in the whole project."""

from django.shortcuts import render_to_response
from django.template import RequestContext, defaultfilters

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_user():
    """Get the current user from local thread.

    Returns:
        The current user's object.

    """
    return getattr(_thread_locals, 'user', None)


def get_current_request():
    """Get the current request from local thread.

    Returns:
        The current request object.

    """
    return getattr(_thread_locals, 'request', None)


class ThreadLocals(object):

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.request = request


def render_template(tmpl, dct=None):
    """Shortcut to the render_to_response Django function.

    This function should be called everytime instead of the render_response
    function in order to handle local threads.


    Returns:
        Response with rendered template.

    """
    return render_to_response(
        tmpl, dct, context_instance=RequestContext(get_current_request()))


def slugify(text):
    """Shortcut to the slugify filter from Django templates.

    Returns:
        Slugified text.

    """
    return defaultfilters.slugify(text)
