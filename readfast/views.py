from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic import TemplateView


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
