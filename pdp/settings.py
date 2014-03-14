# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

import os
import platform
import locale

# Python is platform-independent...or is it?
if platform.system() == "Windows":
    locale.setlocale(locale.LC_TIME, 'fra')
else:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)  # debug toolbar

ADMINS = (
    ('user', 'mail'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'base.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# You need to have yuglify installed, except for DEBUG builds
if DEBUG:
    PIPELINE_JS_COMPRESSOR = None
    PIPELINE_CSS_COMPRESSOR = None

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/vendor/custom.modernizr.js',
            'js/vendor/jquery.js',
            'js/foundation.min.js',
        ),
        'output_filename': 'js/base.js'
    },
    'custom': {
        'source_filenames': {
            'js/custom/ajax-csrf.js',
            'js/custom/editor.js',
            'js/custom/section.js',
        },
        'output_filename': 'js/custom.js'
    },
}

PIPELINE_CSS = {
    'pdp': {
        'source_filenames': (
            'css/progdupeupl.css',
        ),
        'output_filename': 'css/pdp.css',
        'extra_content': {
            'media': 'screen,projection',
        },
    },
    'print': {
        'source_filenames': (
            'css/print.css',
        ),
        'output_filename': 'css/print.css',
        'extra_content': {
            'media': 'print',
        },
    },
}

PIPELINE_DISABLE_WRAPPER = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n!01nl+318#x75_%le8#s0=-*ysw&amp;y49uc#t=*wvi(9hnyii0z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pdp.utils.ThreadLocals',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'pdp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pdp.wsgi.application'

# Absolute path to template directory
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Default context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Custom context processors
    'pdp.utils.context_processors.versions',
    'pdp.utils.context_processors.git_version',
)

INSTALLED_APPS = (
    'pdp.member',
    'pdp.forum',
    'pdp.utils',
    'pdp.pages',
    'pdp.tutorial',
    'pdp.article',
    'pdp.gallery',
    'pdp.messages',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
    'crispy_forms',
    'crispy_forms_foundation',
    'captcha',
    'email_obfuscator',
    'debug_toolbar',
    'taggit',
    'taggit_templatetags',
    'pipeline',
    'rest_framework',
    'provider',
    'provider.oauth2',
    'rest_framework_swagger',
    'haystack',
    'celery',

    # Better use RabbitMQ or Redis in production
    'kombu.transport.django',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Cache(s) used in order to store rendered pages or parts for some time. This
# is a fake cache that does not cache anything, for developement purposes only.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

REST_FRAMEWORK = {

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.YAMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
    ),

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',  # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh'),
    },
}

AUTH_PROFILE_MODULE = 'member.Profile'
LOGIN_URL = '/membres/connexion'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/membres/voir/{0}'.format(
        u.username.encode('utf-8'))
}

CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_TEMPLATE_PACK = 'foundation'

# Bot settings
BOT_ENABLED = False
BOT_USER_PK = 1
BOT_TUTORIAL_FORUM_PK = 1
BOT_ARTICLE_FORUM_PK = 2

# Should Django serve the static and media files ? This should not be set to
# True in a production environment
SERVE = False

# Max size image upload (in bytes)
IMAGE_MAX_SIZE = 1024 * 512

# Do use RabbitMQ or Redis in production
BROKER_URL = 'django://'

# Do not allow pickle in production
CELERY_ACCEPT_CONTENT = ['json', 'pickle']

# Load the production settings, overwrite the existing ones if needed
try:
    from pdp.settings_prod import *
except ImportError:
    pass
