from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

admin.autodiscover()

handler500 = 'main.views.server_error'

urlpatterns = patterns('',
    url(r'^(?P<pubdate>\d{4}-\d{2}-\d{2})/$', 'main.views.home', name="home-date"),
    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    url(r'^$', 'main.views.home', name='home'),
)

urlpatterns += patterns('',
    url(r'^statistics/histdata/', 'statistics.views.histdata', name="statistics-histdata"),
    url(r'^statistics/', 'statistics.views.main', name="statistics-main"),
)

urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/' % settings.WEBSCREENSHOTS_IMAGES_PATH.replace('/', ''), 'main.views.fake_wsimages', name='fake-wsimages'),
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )
