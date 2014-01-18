# coding: utf-8

"""Useful fonctions for dealing with Django's cache system."""

from hashlib import md5


def template_cache_key(identifier, username):
    """Get the template cached content.

    Args:
        identifier: name of the template cache block
        username: user's name

    Returns:
        A key for accessing template's cached content.

    """
    key = 'template.cache.{}.{}'.format(
        identifier,
        md5(username.encode('utf-8')).hexdigest())
    return key
