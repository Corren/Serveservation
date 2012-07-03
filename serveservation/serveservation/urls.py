from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *#jonathan stuff
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#handler404 = 'site_utils.handler404'
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'serveservation.views.home', name='home'),
    # url(r'^serveservation/', include('serveservation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^servers/', include('servers.server-urls')),
    url(r'^reservations/', include('servers.reservation-urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
#    url(r'^login/$', include('auth.views.login_user')), #jonathan stuff
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^accounts/profile/$', 'redirect_to', {'url': 'generic_account_url'}),
)

#urlpatterns += staticfiles_urlpatterns()
