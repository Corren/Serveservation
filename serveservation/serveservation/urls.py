from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'serveservation.views.home', name='home'),
    # url(r'^serveservation/', include('serveservation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^servers/$', 'servers.views.servers'),
    url(r'^reservations/$', 'servers.views.reservations'),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^accounts/profile/$', 'redirect_to', {'url': 'generic_account_url'}),
)

