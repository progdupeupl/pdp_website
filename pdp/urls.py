from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import pages.views
import settings

urlpatterns = patterns('',

    url(r'articles/', include('pdp.article.urls')),
    url(r'^tutoriels/', include('pdp.tutorial.urls')),
    url(r'^forums/', include('pdp.forum.urls')),
    url(r'^membres/', include('pdp.member.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', pages.views.accueil),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
