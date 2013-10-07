from django.conf.urls import patterns, include, url
from django.contrib import admin

import readfast.views


admin.autodiscover()


urlpatterns = patterns('',
    url(r"^read/$",  readfast.views.ReadView.as_view(), name="read"),
    url(r'^tests/', include('readfast.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
