from django.conf.urls import patterns, include, url
from django.contrib import admin

import readfast.views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('readfast.urls')),
    url(r'^admin/$', include(admin.site.urls)),
)
