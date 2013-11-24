# encoding: utf-8

import sys

import django

def versions(request):
    return {
        'django_version': '{0}.{1}.{2}'.format(
            django.VERSION[0], django.VERSION[1], django.VERSION[2]),
        'python_version': '{0}.{1}.{2}'.format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2])
    }


def git_version(request):
    try:
        with open('git_version.txt') as f:
            v = f.read()
    except IOError:
        v = 'local_version'

    return {
        'git_version': v
    }
