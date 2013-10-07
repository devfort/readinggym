from django.conf.urls import patterns, url

import readfast.views

urlpatterns = patterns('',
    url(r"^read/$",  readfast.views.ReadView.as_view(), name="read"),
    url(r"^speedtest/$",  readfast.views.SpeedTestView.as_view(), name="speedtest"),
)
