from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from depot1.views import login_view, logout_view, store_view, register
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', store_view),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('depot1.urls')),
    (r'^accounts/login/$', login_view),
    (r'^accounts/logout/$', logout_view),
    (r'^accounts/register/$', register),
)
