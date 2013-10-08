from django.conf.urls import patterns, url

import readfast.views

urlpatterns = patterns('',
    url(r"^$",  readfast.views.IndexView.as_view(), name="index"),
    url(r"^dashboard/$",  readfast.views.DashboardView.as_view(),
        name="dashboard"),
    url(r"^reading/speed/$",  readfast.views.SpeedTestView.as_view(),
        name="speed-test"),
    url(r"^reading/practice/$",  readfast.views.PracticeReadingView.as_view(),
        name="practice"),
    url(r"^reading/practice/(?P<pk>[0-9]+)/$",  readfast.views.PracticeReadingView.as_view(),
        name="practice"),

    url(r"^reading/sprint/$",  readfast.views.PracticeReadingView.as_view(),
        name="random-sprint"),
    url(r"^reading/sprint/(?P<pk>[0-9]+)/$",  readfast.views.PracticeReadingView.as_view(),
        name="sprint"),

    url(r"^reading/qs/(?P<pk>[0-9]+)/$",
        readfast.views.ComprehensionView.as_view(), name="comprehension"),
)
