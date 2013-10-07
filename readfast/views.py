from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic import TemplateView

from readfast.models import Test


class TestIndexView(View):
    def get(self, request, *args, **kwargs):
        test_list = Test.objects.order_by('-id')
        return render(request, 'readfast/index.html', {'test_list': test_list})


class TestDetailView(View):
    def get(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        return render(request, 'readfast/detail.html', {'test': test})


class ReadView(TemplateView):
    template_name = "read.html"

    def get_context_data(self, **kwargs):
        data = open("riker.corpus")
        words_to_read = []
        for word in data.read().split():
            words_to_read.append("<span>%s </span>" % word)
        words_to_read = "".join(words_to_read)
        context = super(ReadView, self).get_context_data(**kwargs)
        context['words_to_read'] = words_to_read
        return context
