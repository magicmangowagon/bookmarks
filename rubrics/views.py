from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Challenge
from .forms import ChallengeForm, UserFileForm
from django.views.generic import ListView, DetailView
from django import forms


def update_challenge(request):
    challenge = Challenge.objects.get()
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
    else:
        form = ChallengeForm(instance=challenge)
    return render(request, 'rubrics/rubric_form.html', {'form': form, 'challenge': challenge})


class challenge_detail(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(challenge_detail, self).get_context_data(**kwargs)
        context['rubric_list'] = Challenge.objects.all()
        context['form'] = SolutionForm()
        return context


class SolutionForm(forms.Form):
    file = forms.FileField()


class ChallengeListView(ListView):
    queryset = Challenge.objects.all()
    context_object_name = 'challenges'
    # paginate_by = 3
    template_name = 'rubrics/list.html'


def solution_submission(request):
    submitted = False
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            usersolution = form.save(commit=False)
            try:
                usersolution.userOwner = request.user
            except Exception:
                pass
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = UserFileForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'rubrics/solution_form.html', {'form': form, 'submitted': submitted})
