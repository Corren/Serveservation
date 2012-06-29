from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('servers.views',

  url(r'^$', 'all_servers'),
  url(r'^(?P<servername>\w+)/$', 'server_page'),
)
