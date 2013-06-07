# encoding: utf-8

import sys

import django

from pdp import settings

def analytics(request):
    # Try to retrieve the Google Analytics key from settings, if any
    try:
        gak = settings.GOOGLE_ANALYTICS_KEY
    except AttributeError:
        gak = None

    return {'GOOGLE_ANALYTICS_KEY': gak}

def versions(request):
    return {
        'django_version': '%s.%s.%s' % django.VERSION[:3],
        'python_version': '%s.%s.%s' % sys.version_info[:3]
    }
