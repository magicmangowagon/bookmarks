from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Challenge, UserSolution, Rubric, RubricLine
from .forms import ChallengeForm, UserFileForm
from django.views.generic import ListView, DetailView, FormView
from django import forms
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views import View


# Class based challenge view with functioning form.
# Currently using this. Need to revisit, probably not best practice.
class challenge_detail(DetailView, FormMixin):
    template_name = 'rubrics/challenge_detail.html'
    model = Challenge
    form_class = UserFileForm

    def get_success_url(self):
        return reverse('success', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(challenge_detail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        # I don't love this, need to find out if this is an acceptable way to pass user id and challenge name to
        # userSolution model. First attempt commented out directly below. Working version just past it.
        # context['userSolution'] = UserSolution(initial={'userOwner': self.request.user})
        context['form'] = UserFileForm(initial={'challengeName': self.object, 'userOwner': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(challenge_detail, self).form_valid(form)


class SolutionDetailView(DetailView):
    template_name = 'rubrics/solution_detail.html'
    model = UserSolution

    def get_context_data(self, **kwargs):
        context = super(SolutionDetailView, self).get_context_data(**kwargs)
        context['solution_list'] = UserSolution.objects.all()
        return context


class ChallengeListView(ListView):
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    # paginate_by = 3
    template_name = 'rubrics/list.html'


class SolutionListView(ListView):
    queryset = UserSolution.objects.all()
    context_object_name = 'solutions'
    paginate_by = 3
    template_name = 'rubrics/solution_list.html'


class RubricForm(FormView):
    model = Rubric


def success(request, pk):
    return render(request, 'rubrics/success.html', )


# function based view not being used, supplanted by Class based view above
def solution_submission(request, pk):
    submitted = False
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            usersolution = form.save(commit=False)
            try:
                usersolution.userOwner = request.user
                usersolution.challengeName = Challenge.pk
            except Exception:
                pass
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserFileForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'rubrics/solution_form.html', {'form': form, 'submitted': submitted})

