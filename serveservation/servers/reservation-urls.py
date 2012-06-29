from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('servers.views',

  url(r'^$', 'reservations'),
  url(r'^reserve/$', 'reserve_server'),
)
