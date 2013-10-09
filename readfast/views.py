import random
import time
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import (
    FormView, TemplateView, DetailView, RedirectView, View
)
from django.views.generic.edit import ProcessFormView, FormMixin

import readfast.forms as forms
import readfast.models as models


def spanify(text):
    words_to_read = []
    for line in text.splitlines(True):
        for word in line.split():
            words_to_read.append("<span>%s </span>" % word)
        if not line.strip():
            words_to_read.append("<br/>")

    return words_to_read


def session_has_reading_data(session):
    return "reading_speed" in session


class DashboardView(TemplateView):
    """
    /dashboard/

    Shows you some info about how well you read and what to do next.
    """
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        try:
            speeds = self.request.session['reading_speeds']
            latest_speed = speeds[-1]
            improvement = latest_speed - speeds[0]
            context['reading_speeds'] = speeds
            context['reading_improvement'] = improvement

            quickest_speed = float(max(speeds))
            percentages = [speed/quickest_speed*100 for speed in speeds]
            inverted_percentages = [100 - percentage for percentage in percentages]
            context['speeds_and_percentages'] = zip(speeds, percentages, inverted_percentages)
            context['words_read'] = self.request.session.get('words_read')
        except KeyError:
            pass
        return context


class ResetView(View):
    """
    /reset/

    Allows you to delete all of your data.
    """

    def get_context_data(self):
        context = super(ResetView, self).get_context_data()
        context['has_reading_data'] = session_has_reading_data(self.request.session)
        return context

    def post(self, request, **kwargs):
        self.request.session.flush()
        return redirect("dashboard")


class ReadViewMixin(object):
    def get_context_data(self, **kwargs):
        words_to_read = spanify(self.object.text)

        context = super(ReadViewMixin, self).get_context_data(**kwargs)
        context['words_to_read'] = "".join(words_to_read)
        context['wordcount'] = len(words_to_read)
        return context


class RandomRedirectView(RedirectView):
    """
    If the URL doesn't define a particular object to
    use for the detail view. Find one via the magic of
    entropy.
    """

    def get_redirect_url(self, **kwargs):
        random_collection = self.model.objects.order_by('?')
        if random_collection:
            object = random_collection[0]
        else:
            raise self.model.DoesNotExist

        return reverse(self.viewname, kwargs={"pk": object.pk})


class RandomSpeedTestView(RandomRedirectView):
    model = models.Piece
    viewname = "speed-test"


class SpeedTestView(ProcessFormView, FormMixin, ReadViewMixin, DetailView):
    template_name = "speedtest.html"
    form_class = forms.SpeedTestForm
    model = models.Piece

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(SpeedTestView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("comprehension", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(SpeedTestView, self).get_context_data(**kwargs)
        # Cannot do this while constructing form as nees the wordcount
        # from ReadViewMixin.get_context_data
        context['form'].fields['wordcount'].initial = context['wordcount']
        context.setdefault('object', self.object)
        return context

    def form_valid(self, form):
        self.request.session['words_read'] = (
            form.cleaned_data['wordcount'] +
            self.request.session.get('words_read', 0)
        )

        reading_speed = int(form.cleaned_data['wordcount'] / (form.cleaned_data['seconds']/60))
        self.request.session['unchecked_speed'] = reading_speed
        return super(SpeedTestView, self).form_valid(form)


class RandomPracticeReadingView(RandomRedirectView):
    model = models.Piece
    viewname = "practice"


class PracticeReadingView(ReadViewMixin, DetailView):
    """
    /practice/<piece_id>/

    Shows you a piece with a reading regulator.
    """
    template_name = "practice.html"
    model = models.Piece


class RandomSprintView(RandomPracticeReadingView):
    template_name = "sprint.html"


class SprintView(PracticeReadingView):
    template_name = "sprint.html"


class RandomComprehensionView(RandomRedirectView):
    model = models.Piece
    viewname = "comprehension"


class ComprehensionView(DetailView):
    """
    /comprehension/<piece_id>/

    Shows you some questions about the piece and scores you
    """
    template_name = "comprehension.html"
    model = models.Piece

    def get_context_data(self, **kwargs):
        context = super(ComprehensionView, self).get_context_data(**kwargs)
        questions = []
        for q in self.object.questions.order_by('?')[:10]:
            answers = list(
                chain(q.answers.filter(correct=False).order_by('?')[:2],
                      q.answers.filter(correct=True)[:1])
            )
            random.shuffle(answers)
            questions.append((q, answers))
        context['questions'] = questions
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

        reading_speed = self.request.session.get('unchecked_speed')
        if reading_speed:
            del self.request.session['unchecked_speed']

        if correct_answers != num_questions:
            self.template_name = "comprehension_fail.html"
        else:
            self.template_name = "comprehension_pass.html"

            if reading_speed:
                new_speeds = (
                    self.request.session.get('reading_speeds', []) +
                    [reading_speed]
                )
                self.request.session['reading_speeds'] = new_speeds

        response = self.render_to_response(self.get_context_data(**kwargs))

        if reading_speed:
            response.set_cookie("wpm", reading_speed)

        return response
