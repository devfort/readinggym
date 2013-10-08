from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, TemplateView, DetailView

import readfast.forms as forms
import readfast.models as models


def spanify(text):
    words_to_read = []
    for line in text.splitlines():
        for word in line.split():
            words_to_read.append("<span>%s </span>" % word)
        words_to_read.append("\n")

    return words_to_read


class IndexView(TemplateView):
    """
    /

    The homepage.
    """
    template_name = "index.html"


class DashboardView(TemplateView):
    """
    /dashboard/

    Shows you some info about how well you read and what to do next.
    """
    template_name = "dashboard.html"


class ReadViewMixin(object):
    def get_context_data(self, **kwargs):
        data = open("corpora/makers_snippit.txt")
        words_to_read = spanify(data.read())

        context = super(ReadViewMixin, self).get_context_data(**kwargs)
        context['words_to_read'] = "".join(words_to_read)
        context['wordcount'] = len(words_to_read)
        return context


class SpeedTestView(ReadViewMixin, FormView):
    template_name = "speedtest.html"
    form_class = forms.SpeedTestForm
    success_url = '/dashboard'

    def get_context_data(self, **kwargs):
        context = super(SpeedTestView, self).get_context_data(**kwargs)
        context['form'].fields['wordcount'].initial = context['wordcount']
        return context

    def form_valid(self, form):
        # XXX Stash in cookie via session
        # print form.cleaned_data['seconds'] / form.cleaned_data['wordcount']
        return super(SpeedTestView, self).form_valid(form)


class PracticeReadingView(ReadViewMixin, DetailView):
    """
    /practice/<piece_id>/

    Shows you a piece with a reading regulator.
    """
    template_name = "practice.html"
    model = models.Piece


class ComprehensionView(DetailView):
    """
    /comprehension/<piece_id>/

    Shows you some questions about the piece and scores you
    """
    template_name = "comprehension.html"
    model = models.Piece

    def get_context_data(self, **kwargs):
        questions = self.object.questions.order_by('?')[:10]

        context = super(ComprehensionView, self).get_context_data(**kwargs)
        context['questions'] = [(q, q.answers.order_by('?')[:3])
                                for q in questions]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        correct_answers = 0
        num_questions = 0

        for field, value in request.POST.iteritems():
            if field.startswith("q-"):
                qid = int(field[2:])
                aid = int(value)

                correct = self.object.questions.filter(
                    id=qid,
                    answers__correct=True,
                    answers__id=aid,
                )

                correct_answers += bool(correct)
                num_questions += 1

        kwargs['correct_answers'] = correct_answers
        kwargs['num_questions'] = num_questions

        if correct_answers != num_questions:
            self.template_name = "comprehension_fail.html"
        else:
            self.template_name = "comprehension_pass.html"

        return self.render_to_response(self.get_context_data(**kwargs))

