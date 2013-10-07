from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView, DetailView

import readfast.forms as forms
import readfast.models as models

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


class SpeedTestView(FormView):
    template_name = "speedtest.html"
    form_class = forms.SpeedTestForm
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
        # import pdb; pdb.set_trace()
        # Stash in cookie
        print form.cleaned_data['seconds']
        return super(SpeedTestView, self).form_valid(form)


class ReadView(TemplateView):
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


class PracticeReadingView(ReadView):
    """
    /practice/<piece_id>/

    Shows you a piece with a reading regulator.
    """
    template_name = "practice.html"


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

        if correct_answers != num_questions:
            self.template_name = "comprehension_fail.html"
        else:
            self.template_name = "comprehension_pass.html"

        return self.render_to_response(self.get_context_data(**kwargs))
