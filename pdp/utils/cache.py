# coding: utf-8

"""Useful fonctions for dealing with Django's cache system."""

from hashlib import md5

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


def template_cache_delete(fragment_name, vary_on=None):
    """Delete the template cached content.

    Args:
        fragment_name: name of the template cached fragment
        vary_on: list of arguments

    """
    cache.delete(make_template_fragment_key(fragment_name, vary_on))
