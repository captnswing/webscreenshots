from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<pubdate>\d{4}-\d{2}-\d{2})/$', 'main.views.home', name="home-date"),
    url(r'^about/', TemplateView.as_view(template_name="about.html")),
    url(r'^$', 'main.views.home', name='home'),
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
