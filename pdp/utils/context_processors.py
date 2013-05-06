# encoding: utf-8

from pdp import settings

def analytics(request):
    # Try to retrieve the Google Analytics key from settings, if any
    try:
        gak = settings.GOOGLE_ANALYTICS_KEY
    except AttributeError:
        gak = None

    return {'GOOGLE_ANALYTICS_KEY': gak}
