from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView

import readfast.views

urlpatterns = patterns('',
    url(r"^$",  TemplateView.as_view(template_name="index.html"), name="index"),
    url(r"^why/$",  TemplateView.as_view(template_name="why.html"), name="why"),
    url(r"^why/more/$", TemplateView.as_view(template_name="furtherquestions.html"), name="faq"),
    url(r"^about/$",  TemplateView.as_view(template_name="about.html"), name="about"),


    url(r"^dashboard/$", RedirectView.as_view(url="/training/")),

    url(r"^training/$",  readfast.views.DashboardView.as_view(),
        name="dashboard"),

    url(r"^reset/$",  readfast.views.ResetView.as_view(),
        name="reset"),

    url(r"^graphs/$",  readfast.views.GraphsView.as_view(),
        name="graphs"),
    
    url(r"^reading/speed/$",  readfast.views.NextSpeedTestView.as_view(),
        name="speed-test"),
    url(r"^reading/speed/(?P<pk>[0-9]+)/$",  readfast.views.SpeedTestView.as_view(),
        name="speed-test"),

    url(r"^reading/practice/$",  readfast.views.NextPracticeReadingView.as_view(),
        name="practice"),
    url(r"^reading/practice/(?P<pk>[0-9]+)/$",  readfast.views.PracticeReadingView.as_view(),
        name="practice"),

    url(r"^reading/sprint/$",  readfast.views.NextSprintView.as_view(),
        name="random-sprint"),
    url(r"^reading/sprint/(?P<pk>[0-9]+)/$",  readfast.views.SprintView.as_view(),
        name="sprint"),

    url(r"^reading/qs/(?P<pk>[0-9]+)/$",
        readfast.views.ComprehensionView.as_view(), name="comprehension"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
