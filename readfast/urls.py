from django.conf.urls import patterns, url

import readfast.views

urlpatterns = patterns('',
    url(r"^$",  readfast.views.IndexView.as_view(), name="index"),
    url(r"^speed/$",  readfast.views.SpeedTestView.as_view(), name="speed-test"),
    url(r"^reading/practice/$",  readfast.views.PracticeReadingView.as_view(), name="practice"),
)
