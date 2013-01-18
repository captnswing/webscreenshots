from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<pubdate>\d{4}-\d{2}-\d{2})/$', 'main.views.home', name="home-date"),
    url(r'^$', 'main.views.home', name='home'),
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
