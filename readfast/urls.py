from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

import readfast.views

urlpatterns = patterns('',
    url(r"^$",  readfast.views.IndexView.as_view(), name="index"),
    url(r"^why/$",  readfast.views.WhyView.as_view(), name="why"),


    url(r"^dashboard/$", RedirectView.as_view(url="/training/")),

    url(r"^training/$",  readfast.views.DashboardView.as_view(),
        name="dashboard"),

    url(r"^reset/$",  readfast.views.ResetView.as_view(),
        name="reset"),

    url(r"^reading/speed/$",  readfast.views.RandomSpeedTestView.as_view(),
        name="speed-test"),
    url(r"^reading/speed/(?P<pk>[0-9]+)/$",  readfast.views.SpeedTestView.as_view(),
        name="speed-test"),

    url(r"^reading/practice/$",  readfast.views.RandomPracticeReadingView.as_view(),
        name="practice"),
    url(r"^reading/practice/(?P<pk>[0-9]+)/$",  readfast.views.PracticeReadingView.as_view(),
        name="practice"),

    url(r"^reading/sprint/$",  readfast.views.RandomSprintView.as_view(),
        name="random-sprint"),
    url(r"^reading/sprint/(?P<pk>[0-9]+)/$",  readfast.views.SprintView.as_view(),
        name="sprint"),

    url(r"^reading/qs/(?P<pk>[0-9]+)/$",
        readfast.views.ComprehensionView.as_view(), name="comprehension"),
)
