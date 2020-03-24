from django.shortcuts import render
from rubrics.models import UserSolution, Challenge, Evaluated
from account.models import Profile
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, FormView


# Create your views here.
class NewSolutionDispatch(ListView):
    context_object_name = 'newSolutions'
    queryset = UserSolution.objects.all().filter(evaluated__isnull=True)
    template_name = 'centralDispatch/newSolutionDispatch.html'

    def get_context_data(self, **kwargs):
        context = super(NewSolutionDispatch, self).get_context_data()
        challenges = Challenge.objects.all().filter(display=True).order_by('challengeGroupChoices')
        context['challenges'] = challenges
        return context
