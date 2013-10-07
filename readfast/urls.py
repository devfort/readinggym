from django.conf.urls import patterns, url

import readfast.views

urlpatterns = patterns('',
    url(r"^read/$",  readfast.views.ReadView.as_view(), name="read"),
)
