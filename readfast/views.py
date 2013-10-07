from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"


class ReadSetupView(TemplateView):
    template_name = "read_setup.html"


class SpeedTestView(TemplateView):
    template_name = "speed_test.html"


class ReadView(TemplateView):
    template_name = "read.html"

    def get_context_data(self, **kwargs):
        data = open("corpae/makers_snippit.txt")
        words_to_read = []
        for line in data:
            words_to_read.append("\n")
            for word in line.split():
                words_to_read.append("<span>%s </span>" % word)

        words_to_read = "".join(words_to_read)
        context = super(ReadView, self).get_context_data(**kwargs)
        context['words_to_read'] = words_to_read
        return context


class ComprehensionView(FormView):
    template_name = "comprehension.html"

