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

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.models import User, Group

from haystack.views import SearchView
from haystack.forms import ModelSearchForm

from rest_framework import viewsets, routers

from django.contrib import admin
admin.autodiscover()

import pdp.pages.views
import pdp.settings

# ViewSets define the view behavior.

class UserViewSet(viewsets.ModelViewSet):
    model = User


class GroupViewSet(viewsets.ModelViewSet):
    model = Group


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns(
    '',

    url(r'^articles/', include('pdp.article.urls')),
    url(r'^tutoriels/', include('pdp.tutorial.urls')),
    url(r'^forums/', include('pdp.forum.urls')),
    url(r'^messages/', include('pdp.messages.urls')),
    url(r'^membres/', include('pdp.member.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('pdp.pages.urls')),
    url(r'^galerie/', include('pdp.gallery.urls')),
    url(r'^api/', include('pdp.api.urls')),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^$', pdp.pages.views.home),

    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),

    url(r'^recherche/', SearchView(
        template='search/search.html',
        form_class=ModelSearchForm),
        name='haystack_search'),

    url(r'^robots\.txt$', pdp.pages.views.robots),

) + static(pdp.settings.MEDIA_URL, document_root=pdp.settings.MEDIA_ROOT)

# Serve debug toolbar files on debug
if pdp.settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)))

# Make Django serve the files if needed (local versions)
if pdp.settings.SERVE:
    urlpatterns += patterns(
        '',

        # Static content for website assets
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': pdp.settings.STATIC_ROOT}),

        # User-uploaded content
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': pdp.settings.MEDIA_ROOT}),
    )
