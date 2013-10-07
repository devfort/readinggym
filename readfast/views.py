from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView, View
# import readfast.forms

from readfast.forms import SpeedTestForm

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

class SpeedTestView(FormView):
    template_name = "speedtest.html"
    form_class = SpeedTestForm
    success_url = 'FIXME-Now-go-test'

    def get_context_data(self, **kwargs):
        data = open("corpae/makers_snippit.txt")
        words_to_read = []
        for word in data.read().split():
            words_to_read.append("<span>%s </span>" % word)
        words_to_read = "".join(words_to_read)
        context = super(SpeedTestView, self).get_context_data(**kwargs)
        context['words_to_read'] = words_to_read
        context['wordcount'] = words_to_read.count
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        import pdb; pdb.set_trace()
        print form.cleaned_data['seconds']
        return super(SpeedTestView, self).form_valid(form)

